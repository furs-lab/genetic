import logging
from logging.config import dictConfig
import jinja2

import calculations
import plotrisk
from analysis import Analysis
from config import logging_config, files, latex_jinja_env
import os

if __name__ == '__main__':
    dictConfig(logging_config)

    logging.info("start main")
    analysis = Analysis("tst_analysis.xlsx")
    panels = analysis.get_panels()
    # analysis.get_panel_data('fat')
    analysis.sort_by_gens()
    print(analysis.data['Gen'].tolist())

    import database

    template = latex_jinja_env.get_template(files['template_name'])

    temp_vars = calculations.create_jinja2_dict(analysis)

    res = template.render(temp_vars)

    with open(files['template_path'] + files['output_name'], 'w') as f:
        f.write(res)
    f.close()

    database.stop()
    logging.info("finish main")
