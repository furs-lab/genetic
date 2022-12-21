import decimal

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, relationship, sessionmaker
import logging
from multipledispatch import dispatch
from dbclasses import *

dbsession = sessionmaker(bind=engine)
session = dbsession()
logging.info(f'start data base session')


def stop():
    session.close()
    engine.dispose()
    logging.info(f'close database session')


def gen_query_to_list(qr):
    res = []
    for row in qr.all():
        res.append(row.__dict__)
        del res[-1]['_sa_instance_state']
        res[-1] = {k: float(v) if isinstance(v, decimal.Decimal) else v for k, v in res[-1].items()}
    return res

@dispatch(str)
def get_gene(gene_name):
    qr = session.query(Genes).filter(Genes.name == gene_name)
    gene = gen_query_to_list(qr)
    if len(gene) > 1:
        rs_pos = [row.rs_position for row in qr.all()]
        logging.warning(f'more than one gene found because there are several rs_positions {rs_pos}')
    if len(gene) == 0:
        logging.warning(f'gene: \'{gene_name}\' does not exist, empty list returned')
    logging.info(f'get gene: \'{gene_name}\'')
    return gene


@dispatch(str, str)
def get_gene(gene_name, rs_pos):
    qr = session.query(Genes).filter(Genes.name == gene_name).filter(Genes.rs_position == rs_pos)
    gene = gen_query_to_list(qr)
    if len(gene) == 0:
        logging.warning(f'gene: \'{gene_name}\', rs_position: \'{rs_pos}\' does not exist, empty list returned')
    logging.info(f'get gene: \'{gene_name}\', rs_position: \'{rs_pos}\'')
    return gene


@dispatch(int)
def get_gene(gene_id):
    qr = session.query(Genes).filter(Genes.id == gene_id)
    gene = gen_query_to_list(qr)
    if len(gene) == 0:
        logging.warning(f'gene with id: \'{gene_id}\' does not exist, empty list returned')
    logging.info(f'get gene with id: {gene_id}')
    return gene


@dispatch(str)
def get_themes(panel_name):
    qr = session.query(Panels, PanelSet).filter(Panels.id == PanelSet.id_panel).filter(Panels.name == panel_name)
    themes_list = []
    for row in qr.all():
        themes_list.append({'id': row.PanelSet.id_theme,
                            'name': session.get(Themes, row.PanelSet.id_theme).name,
                            'name_report': session.get(Themes, row.PanelSet.id_theme).name_report,
                            'order': row.PanelSet.order_theme,
                            'visible': row.PanelSet.visible_theme})
    if len(themes_list) == 0:
        logging.warning(f'no themes in this panel: \'{panel_name}\', empty themes list is returned')
    logging.info(f'get themes list {[itm["id"] for itm in themes_list]} for panel \'{panel_name}\'')
    return themes_list


@dispatch(int)
def get_themes(panel_id):
    if session.get(Panels, panel_id) is not None:
        panel_name = session.get(Panels, panel_id).name
        return get_themes(panel_name)
    else:
        logging.warning(f'there are no panel with id: {panel_id}, empty themes list is returned')
        return []


def get_subthemes(theme_id):
    qr = session.query(ThemeSet, SubThemes).filter(SubThemes.id == ThemeSet.id_subtheme).filter(
        ThemeSet.id_theme == theme_id)
    subthemes_list = []
    for row in qr.all():
        subthemes_list.append(row.SubThemes.__dict__)
        subthemes_list[-1].update({'order': row.ThemeSet.order_subtheme})
        del subthemes_list[-1]['_sa_instance_state']
    if len(subthemes_list) == 0:
        logging.warning(f'there is no subthemes for theme with id: {theme_id}, empty themes list is returned')
    logging.info(f'get subthemes list {[itm["id"] for itm in subthemes_list]} for theme with id: {theme_id}')
    return subthemes_list


def get_risks(subtheme_id):
    qr = session.query(SubThemeSet, Risks).filter(Risks.id == SubThemeSet.id_risk).filter(
        SubThemeSet.id_subtheme == subtheme_id)
    risks_list = []
    for row in qr.all():
        risks_list.append(row.Risks.__dict__)
        risks_list[-1].update({'order': row.SubThemeSet.order_risk})
        del risks_list[-1]['_sa_instance_state']
        risks_list[-1] = {k: float(v) if isinstance(v, decimal.Decimal) else v for k, v in risks_list[-1].items()}
    if len(risks_list) == 0:
        logging.warning(f'there is no risks for subtheme with id: {subtheme_id}, empty risks list is returned')
    logging.info(f'get risks list (ids:  {[itm["id"] for itm in risks_list]}) for subtheme with id: {subtheme_id}')
    return risks_list


def get_genes_for_risk(risk_id):
    qr = session.query(RiskSet).filter(RiskSet.id_risk == risk_id)
    genes_list = []
    for row in qr.all():
        genes_list.append(row.__dict__)
        genes_list[-1].update(get_gene(row.id_gene)[0])
        del genes_list[-1]['_sa_instance_state']
        genes_list[-1] = {k: float(v) if isinstance(v, decimal.Decimal) else v for k, v in genes_list[-1].items()}
    if len(genes_list) == 0:
        logging.warning(f'there is no genes for risk id: {risk_id}, empty genes list is returned')
    logging.info(f'get genes list (ids: {[itm["id"] for itm in genes_list]}) for risk with id: {risk_id}')
    return genes_list
