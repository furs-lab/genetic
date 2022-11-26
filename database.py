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


def get_gene(gene_name, rs_pos=None):
    qr = session.query(Genes).filter(Genes.name == gene_name)
    if rs_pos is not None:
        qr = qr.filter(Genes.rs_position == rs_pos)
    gene = [row.__dict__ for row in qr.all()]
    if len(gene) > 1:
        rs_pos = [row.rs_position for row in qr.all()]
        logging.warning(f'more than one gene found because there are several rs_positions {rs_pos}')
    if len(gene) == 0:
        logging.warning(f'gene: \'{gene_name}\', rs_position: \'{rs_pos}\' does not exist, empty list returned')
        gene = []
    logging.info(f'get gene: \'{gene_name}\', rs_position: \'{rs_pos}\'')
    return gene


@dispatch(str)
def get_themes(panel_name):
    qr = session.query(Panels, PanelSet).filter(Panels.id == PanelSet.id_panel).filter(Panels.name == panel_name)
    themes_list = []
    for row in qr.all():
        themes_list.append({'id': row.PanelSet.id_theme,
                            'name': session.get(Themes, row.PanelSet.id_theme).name,
                            'name_report': session.get(Themes, row.PanelSet.id_theme).name_report})
    if len(themes_list) == 0:
        logging.warning(f'no themes in this panel: \'{panel_name}\', empty themes list is returned')
    logging.info(f'get themes list {[itm["name"] for itm in themes_list]} for panel \'{panel_name}\'')
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
    subthemes_list = [row.SubThemes.__dict__ for row in qr.all()]
    if len(subthemes_list) == 0:
        logging.warning(f'there is no subthemes for theme with id: {theme_id}, empty themes list is returned')
    logging.info(f'get subthemes list {[itm["name"] for itm in subthemes_list]} for theme with id: {theme_id}')
    return subthemes_list


def get_risks(subtheme_id):
    qr = session.query(SubThemeSet, Risks).filter(Risks.id == SubThemeSet.id_risk).filter(
        SubThemeSet.id_subtheme == subtheme_id)
    risks_list = [row.Risks.__dict__ for row in qr.all()]
    if len(risks_list) == 0:
        logging.warning(f'there is no risks for subtheme with id: {subtheme_id}, empty risks list is returned')
    logging.info(f'get risks list {[itm["id"] for itm in risks_list]} for subtheme with id: {subtheme_id}')
    return risks_list
