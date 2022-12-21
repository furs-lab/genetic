import logging
from logging.config import dictConfig
import jinja2
import json
from pathlib import Path

import calculations
import config
import plotrisk
from analysis import Analysis
from config import logging_config, files, latex_jinja_env


def create_json(analysis_fname):
    logging.info("start create_json")
    analysis = Analysis(analysis_fname)
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


def create_tex(analysis_fname):
    logging.info("start create_tex")
    analysis = Analysis(analysis_fname)
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

    create_json("tst_analysis.xlsx")

    # analysis = Analysis("tst_analysis.xlsx")
    # panels = analysis.get_panels()
    # # analysis.get_panel_data('fat')
    # analysis.sort_by_gens()
    #
    # import database
    #
    # template = latex_jinja_env.get_template(files['template_name'])
    #
    # tag_dict = calculations.create_tag_dict(analysis)
    #
    # # Output to TEX
    # res = template.render(tag_dict)
    # fname = Path(config.files['template_path'], config.files['output_tex_name'])
    # with open(fname, 'w') as f:
    #     f.write(res)
    #     logging.info(f'write template file {fname}')
    # f.close()
    #
    # # Output to JSON
    # fname = Path(config.files['template_path'], config.files['output_json_name'])
    # with open(fname, 'w') as f:
    #     del tag_dict['scandat']
    #     json.dump(tag_dict, f)
    #     logging.info(f'write JSON file {fname}')
    # f.close()
    #
    # database.stop()
    logging.info("finish main")
