import logging
from logging.config import dictConfig
import jinja2

import calculations
import plotrisk
from analysis import Analysis
from config import LOGGING_CONFIG, JINJA2_CONFIG, FILES

if __name__ == '__main__':
    dictConfig(LOGGING_CONFIG)
    latex_jinja_env = jinja2.Environment(JINJA2_CONFIG)

    logging.info("start main")
    analysis = Analysis("tst_analysis.xlsx")
    panels = analysis.get_panels()
    # analysis.get_panel_data('fat')
    analysis.sort_by_gens()
    print(analysis.data['Gen'].tolist())

    import database
    res = database.get_risks(8)
    #print(res)
    res1 = calculations.calc_risk(res, analysis)
    print(res1)
    res2 = calculations.modify_risks_dict(res, res1)
    for rr in res2:
        print(rr['inter'])

    database.stop()
    logging.info("finish main")
