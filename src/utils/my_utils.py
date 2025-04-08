import datetime
import os
import random

from src.utils.logger import LogManager
from src.clients.ai_controller import AIController
from src.config.database import SessionLocal
from src.config.config import Config

config = Config()
ai_controller = AIController()
logger = LogManager()
# db = SessionLocal()


class MyUtils:
    """_summary_"""

    # def __init__(self, db: SessionLocal = None):
    #     self.db = db

    async def prepare_message(self, msg=None, prompt=None):
        if prompt is not None and ai_controller.has_service:
            try:
                logger.info("Generating text by AI...")
                msg = await ai_controller.generate_text(prompt)
                logger.info("Generated text by AI: " + str(msg))
            except Exception as e:
                logger.info("Error generating text by AI: " + str(e))
                # msg = msg
        # else:
        #     logger.info("Sending default message...")
        msg = self.format_text_for_md2(msg)
        return msg

    def format_text_for_md2(self, text: str):
        # Comes from old code. Just keeps the text as is for now.
        return text

    def get_date(self) -> datetime.date:
        return datetime.datetime.now().date()
