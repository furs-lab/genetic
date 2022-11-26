import logging
from logging.config import dictConfig
from analysis import Analysis
from logger_config import LOGGING_CONFIG

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dictConfig(LOGGING_CONFIG)

    logging.info("start main")
    Analysis.read(Analysis, "tst_analysis.xlsx")
    panels = Analysis.get_panels(Analysis)
    Analysis.get_panel_data(Analysis, 'fat')
    Analysis.sort_by_gens(Analysis)
    print(Analysis.data['Gen'].tolist())

    import database

    res = database.get_subthemes_id(10)
    print(res)
    database.stop()
    logging.info("finish main")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
