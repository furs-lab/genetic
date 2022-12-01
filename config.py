FILES = {'template_path': './tex/',
         'template_name': 'template01.tex',
         'output_file_name': 'report01.tex'}

# logger config
LOGGING_CONFIG = {
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
JINJA2_CONFIG = {
    'block_start_string': '\BLOCK{',
    'block_end_string': '}',
    'variable_start_string': '\VAR{',
    'variable_end_string': '}',
    'comment_start_string': '\#{',
    'comment_end_string': '}',
    'line_statement_prefix': '%%',
    'line_comment_prefix': '%#',
    'trim_blocks': 'True',
    'autoescape': 'False',
    'loader': 'jinja2.FileSystemLoader(os.path.abspath("."))'
}