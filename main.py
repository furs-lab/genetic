import logging
from logging.config import dictConfig
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

    res = database.get_risks(7)
    print(res)
    for rr in res:
        print(rr['id'], rr['name'], rr['description'])
    database.stop()
    logging.info("finish main")
