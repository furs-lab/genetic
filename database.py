from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, relationship, sessionmaker
import logging


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


def get_gene_function(gene, rs_pos=None):
    qr = session.query(Genes).filter(Genes.name == gene)
    if rs_pos is not None:
        qr = qr.filter(Genes.rs_position == rs_pos)
    gene_func = [row.function for row in qr.all()]
    if len(gene_func) > 1:
        rs_pos = [row.rs_position for row in qr.all()]
        logging.warning(f'more than one gene function find because there are several rs_positions {rs_pos}')
    if len(gene_func) == 0:
        logging.warning(f'gene: \'{gene}\', rs_position: \'{rs_pos}\' does not exist, empty function returned')
        gene_func = ['']
    logging.info(f'get function for gene: \'{gene}\', rs_position: \'{rs_pos}\'')
    return gene_func


def get_themes_id(panel):
    qr = session.query(Panels, PanelSet).filter(Panels.id == PanelSet.id_panel).filter(Panels.name == panel)
    themes = [row.PanelSet.id_theme for row in qr.all()]
    if len(themes) == 0:
        logging.warning(f'no themes in this panel: \'{panel}\', empty thems_id list returned')
    logging.info(f'get them_id list {themes} for panel \'{panel}\'')
    return themes
