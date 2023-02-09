from jinja2 import Environment, FileSystemLoader
from pathlib import Path

files = {'template_path': Path(Path().absolute(), 'tex'),
         'template_name': 'template01.tex',
         'output_tex_name': 'report01.tex',
         'output_json_name': 'report01.json',
         'login_name': 'login_loc.txt'}
# files = {'template_path': Path(Path().absolute(), 'tex'),
#          'template_name': 'template01.tex',
#          'output_tex_name': 'report01.tex',
#          'output_json_name': 'report01.json'}

# logger config
logging_config = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'INFO',
            'handlers': ['console_handler', 'file_handler'],
        },
    },
    'handlers': {
        'console_handler': {
            'level': 'INFO',
            'formatter': 'console_formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'file_handler': {
            'level': 'INFO',
            'formatter': 'file_formatter',
            'class': 'logging.FileHandler',
            'filename': 'genetic.log',
            'mode': 'w',
        },
    },
    'formatters': {
        'console_formatter': {
            'format': '%(levelname)s - %(filename)s:%(funcName)s - %(message)s'
        },
        'file_formatter': {
            'format': '%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)s - %(message)s'
        },
    },
}

# jinja config
latex_jinja_env = Environment(
        block_start_string='\BLOCK{',
        block_end_string='}',
        variable_start_string='\VAR{',
        variable_end_string='}',
        comment_start_string='\#{',
        comment_end_string='}',
        line_statement_prefix='%%',
        line_comment_prefix='%#',
        trim_blocks=True,
        autoescape=False,
        loader=FileSystemLoader(files['template_path'])
    )
