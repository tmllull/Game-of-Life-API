import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler

# from src.database.database import SessionLocal


# db = SessionLocal()
class LogManager:
    def __init__(self, log_dir="logs", log_level=logging.INFO):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        if not self.logger.hasHandlers():
            file_handler = TimedRotatingFileHandler(
                os.path.join(log_dir, "logs"),
                when="midnight",
                interval=1,
                backupCount=7,
                encoding="utf-8",
            )
            file_handler.suffix = "%Y-%m-%d"
            file_handler.setLevel(log_level)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)

            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    # def get_logger(self):
    #     return self.logger

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def exception(self, msg):
        self.logger.exception(msg)

    def error(self, msg):
        self.logger.error(msg)
