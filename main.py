# This is a sample Python script.
import os.path
import logging.config
import yaml

BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, "logs")
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
DATABASE_CONFIG_FILE = os.path.join(BASE_DIR, "conf", "database.yaml")
DATABASE_CONFIG = yaml.load(open(DATABASE_CONFIG_FILE, "r", encoding="UTF-8"), Loader=yaml.FullLoader)

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "class": "logging.Formatter",
                "format": "[%(asctime)s][%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": f"{os.path.join(LOG_DIR, 'server.log')}",
                "maxBytes": 10485760,
                "backupCount": 50,
                "encoding": "utf8",
            }
        },
        "loggers": {},
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"]
        },
    }
)
if __name__ == '__main__':
    print(DATABASE_CONFIG)
