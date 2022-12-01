import logging
from logging.config import dictConfig

import calculations
import plotrisk
from analysis import Analysis
from logger_config import LOGGING_CONFIG

if __name__ == '__main__':
    dictConfig(LOGGING_CONFIG)

    logging.info("start main")
    analysis = Analysis("tst_analysis.xlsx")
    panels = analysis.get_panels()
    # analysis.get_panel_data('fat')
    analysis.sort_by_gens()
    print(analysis.data['Gen'].tolist())

    import database
    import calculations

    res = database.get_risks(8)
    #print(res)
    res1 = calculations.calc_risk(res, analysis)
    print(res1)
    res2 = calculations.modify_risks_dict(res, res1)
    for rr in res2:
        print(rr['inter'])

    database.stop()
    logging.info("finish main")
