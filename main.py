import logging
from logging.config import dictConfig

import plotrisk
from analysis import Analysis
from logger_config import LOGGING_CONFIG

if __name__ == '__main__':
    dictConfig(LOGGING_CONFIG)

    logging.info("start main")
    Analysis.read(Analysis, "tst_analysis.xlsx")
    panels = Analysis.get_panels(Analysis)
    Analysis.get_panel_data(Analysis, 'fat')
    Analysis.sort_by_gens(Analysis)
    print(Analysis.data['Gen'].tolist())

    import database
    import plotrisk

    plotrisk.plot_risk(0.3, 2.7, 1.2)
    res = database.get_themes(13)
    print(res)
    for rr in res:
        print(rr['id'], rr['name'])
    database.stop()
    logging.info("finish main")
