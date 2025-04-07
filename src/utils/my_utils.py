import datetime
import os
import random

import src.utils.logger as logger
from src.clients.ai_controller import AIController
from src.database.database import SessionLocal
from src.utils.config import Config

config = Config()
ai_controller = AIController()
# db = SessionLocal()

# leaving_gifs = [
#     "CgACAgQAAx0CboIgbAACDO9mGWRx5aGU3t41YI9Yq09Bpr4VUgAC9wIAAlx1hVOKzWaxi1UfPjQE",
#     "CgACAgQAAx0CboIgbAACDPJmGWWyJoHT8j3LujDLI1yGGqKtrQAC9QIAAuIXBFOxPQS1SLBLHDQE",
#     "CgACAgQAAx0CboIgbAACDPNmGWXLAzWDlvIjK4RguK-0RMWBeQACIAMAAjG9JFOis1aOwCU45TQE",
#     "CgACAgQAAx0CboIgbAACDPZmGWXqPTo5LhYS8cv2NHGhxWH8LwACMAMAAnxsFFPbZIBe-cVFwTQE",
# ]


class MyUtils:
    """_summary_"""

    def __init__(self, db: SessionLocal = None):
        self.db = db

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
