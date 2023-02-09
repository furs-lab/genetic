from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper
from config import files


class Clinics:
    pass


class Panels:
    pass


class PanelSet:
    pass


class Genes:
    pass


class Themes:
    pass


class ThemeSet:
    pass


class SubThemes:
    pass


class SubThemeSet:
    pass


class Risks:
    pass


class RiskSet:
    pass


with open(files['login_name'], 'r') as f:
    login_str = f.readline()
engine = create_engine(login_str)
# engine = create_engine('mysql+pymysql://root:feromon@localhost/genetic')
meta = MetaData(engine)

clinics = Table('clinics', meta, autoload=True)
panels = Table('panels', meta, autoload=True)
panel_set = Table('panel_set', meta, autoload=True)
genes = Table('genes', meta, autoload=True)
themes = Table('themes', meta, autoload=True)
theme_set = Table('theme_set', meta, autoload=True)
subthemes = Table('subthemes', meta, autoload=True)
subtheme_set = Table('subtheme_set', meta, autoload=True)
risks = Table('risks', meta, autoload=True)
risk_set = Table('risk_set', meta, autoload=True)

mapper(Clinics, clinics)
mapper(Panels, panels)
mapper(PanelSet, panel_set)
mapper(Genes, genes)
mapper(Themes, themes)
mapper(ThemeSet, theme_set)
mapper(SubThemes, subthemes)
mapper(SubThemeSet, subtheme_set)
mapper(Risks, risks)
mapper(RiskSet, risk_set)
