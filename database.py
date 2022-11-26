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


def get_gene_function(gene_name, rs_pos=None):
    qr = session.query(Genes).filter(Genes.name == gene_name)
    if rs_pos is not None:
        qr = qr.filter(Genes.rs_position == rs_pos)
    gene_func = [row.function for row in qr.all()]
    if len(gene_func) > 1:
        rs_pos = [row.rs_position for row in qr.all()]
        logging.warning(f'more than one gene function find because there are several rs_positions {rs_pos}')
    if len(gene_func) == 0:
        logging.warning(f'gene: \'{gene_name}\', rs_position: \'{rs_pos}\' does not exist, empty function returned')
        gene_func = ['']
    logging.info(f'get function for gene: \'{gene_name}\', rs_position: \'{rs_pos}\'')
    return gene_func


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
    logging.info(f'get themes list {themes_list} for panel \'{panel_name}\'')
    return themes_list


@dispatch(int)
def get_themes_id(panel_id):
    qr = session.query(PanelSet).filter(PanelSet.id_panel == panel_id)
    themes_id = [row.id_theme for row in qr.all()]
    if len(themes_id) == 0:
        logging.warning(f'there is no themes for panel with id: {panel_id}, empty themes_id list is returned')
    logging.info(f'get theme_id list {themes_id} for panel with id: {panel_id}')
    return themes_id


def get_subthemes_id(theme_id):
    qr = session.query(ThemeSet).filter(ThemeSet.id_theme == theme_id)
    subthemes_id = [row.id_subtheme for row in qr.all()]
    if len(subthemes_id) == 0:
        logging.warning(f'there is no subthemes for theme with id: {theme_id}, empty themes_id list is returned')
    logging.info(f'get subthemes_id list {subthemes_id} for theme with id: {theme_id}')
    return subthemes_id
