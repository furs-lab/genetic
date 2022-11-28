from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper


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

engine = create_engine('mysql+pymysql://debian-sys-maint:UmX4EHHEbeT8Ad0F@localhost/genetic')
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

mapper(Clinics, clinics)
mapper(Panels, panels)
mapper(PanelSet, panel_set)
mapper(Genes, genes)
mapper(Themes, themes)
mapper(ThemeSet, theme_set)
mapper(SubThemes, subthemes)
mapper(SubThemeSet, subtheme_set)
mapper(Risks, risks)
