from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, relationship, sessionmaker
import logging
from multipledispatch import dispatch


class Clinics:
    pass


class Panels:
    pass


class PanelSet:
    pass


class Genes:
    pass


# engine = create_engine('mysql+pymysql://debian-sys-maint:UmX4EHHEbeT8Ad0F@localhost/genetic')
engine = create_engine('mysql+pymysql://root:feromon@localhost/genetic')
meta = MetaData(engine)

clinics = Table('clinics', meta, autoload=True)
panels = Table('panels', meta, autoload=True)
panel_set = Table('panel_set', meta, autoload=True)
genes = Table('genes', meta, autoload=True)

mapper(Clinics, clinics)
mapper(Panels, panels)
mapper(PanelSet, panel_set)
mapper(Genes, genes)

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
def get_themes_id(panel_name):
    qr = session.query(Panels, PanelSet).filter(Panels.id == PanelSet.id_panel).filter(Panels.name == panel_name)
    themes = [row.PanelSet.id_theme for row in qr.all()]
    if len(themes) == 0:
        logging.warning(f'no themes in this panel: \'{panel_name}\', empty themes_id list is returned')
    logging.info(f'get theme_id list {themes} for panel \'{panel_name}\'')
    return themes


@dispatch(int)
def get_themes_id(panel_id):
    panel_name = session.query(Panels).filter(Panels.id == panel_id).first()
    if panel_name is not None:
        return get_themes_id(panel_name.name)
    else:
        logging.warning(f'there is no panel with id: {panel_id}, empty themes_id list is returned')
        return []
