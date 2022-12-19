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

if __name__ == '__main__':
    dictConfig(logging_config)

    logging.info("start main")
    analysis = Analysis("tst_analysis.xlsx")
    panels = analysis.get_panels()
    # analysis.get_panel_data('fat')
    analysis.sort_by_gens()

    import database

    template = latex_jinja_env.get_template(files['template_name'])

    tag_dict = calculations.create_tag_dict(analysis)

    # Output to TEX
    res = template.render(tag_dict)
    fname = Path(config.files['template_path'], config.files['output_tex_name'])
    with open(fname, 'w') as f:
        f.write(res)
        logging.info(f'write template file {fname}')
    f.close()

    # Output to JSON
    fname = Path(config.files['template_path'], config.files['output_json_name'])
    with open(fname, 'w') as f:
        del tag_dict['scandat']
        json.dump(tag_dict, f)
        logging.info(f'write JSON file {fname}')
    f.close()

    database.stop()
    logging.info("finish main")
