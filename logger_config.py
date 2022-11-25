from logging.config import dictConfig

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
