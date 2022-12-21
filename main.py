import logging
from logging.config import dictConfig
import jinja2
import json
from pathlib import Path
from pandas import read_excel, read_json

import calculations
import config
import plotrisk
from analysis import Analysis
from config import logging_config, files, latex_jinja_env


def analysis_from_excel(fname):
    try:
        analysis_data = read_excel(fname).dropna()
    except Exception:
        logging.exception('Error: can not read excel file')
        raise Exception('Error: can not read excel file')
    logging.info(f'read excel file \'{fname}\'')
    return Analysis(analysis_data)


def json_from_excel(fname):
    try:
        analysis_data = read_excel(fname).dropna()
    except Exception:
        logging.exception('Error: can not read excel file')
        raise Exception('Error: can not read excel file')
    logging.info(f'read excel file \'{fname}\'')
    return analysis_data.to_json()


def analysis_from_json(json_str):
    return Analysis(read_json(json_str))


def create_json_test():
    dic = {'name': 'aaaaa', 'result': 5}
    return dic
def create_json(analysis):
    logging.info("start create_json")
    panels = analysis.get_panels()
    analysis.sort_by_gens()

    import database

    tag_dict = calculations.create_tag_dict(analysis)

    fname = Path(config.files['template_path'], config.files['output_json_name'])
    with open(fname, 'w') as f:
        del tag_dict['scandat']
        json.dump(tag_dict, f)
        logging.info(f'write JSON file {fname}')
    f.close()
    logging.info("finish create_json")
    database.stop()


def create_tex(analysis):
    logging.info("start create_tex")
    panels = analysis.get_panels()
    analysis.sort_by_gens()

    import database

    template = latex_jinja_env.get_template(files['template_name'])
    tag_dict = calculations.create_tag_dict(analysis)
    tag_dict = calculations.process_all_text_in_dict(tag_dict, calculations.process_text)
    calculations.create_risk_figures(tag_dict)

    res = template.render(tag_dict)
    fname = Path(config.files['template_path'], config.files['output_tex_name'])
    with open(fname, 'w') as f:
        f.write(res)
        logging.info(f'write template file {fname}')
    f.close()
    database.stop()
    logging.info("finish create_tex")


if __name__ == '__main__':
    dictConfig(logging_config)

    logging.info("start main")

    analysis = analysis_from_excel("tst_analysis.xlsx")

    create_json(analysis)

    logging.info("finish main")
