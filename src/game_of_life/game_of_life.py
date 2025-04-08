import ast
import random

import src.utils.messages as msgs
import src.utils.prompts as prompts
from sqlalchemy import func
from src.database import models as db_models
from src.config.database import SessionLocal
from src.game_of_life.ecosystem import Ecosystem
from src.utils.logger import LogManager
from src.config.config import Config
from src.utils.my_utils import MyUtils
from src.models import models

utils = MyUtils()
config = Config()
db = SessionLocal()
ecosystem = Ecosystem()
logger = LogManager()


class GameOfLife:
    def __init__(self):
        logger.info("Starting game of life...")

    async def check_evolution(self, request: models.EvolutionRequest):
        try:
            ecosystems_db = self.get_ecosystems_count()
            ecosystem_alive = self.get_alive_ecosystem()

            if ecosystem_alive is None or ecosystems_db == 0:
                logger.info("No ecosystems alive")
                return await self.handle_new_ecosystem(request)
                # db.query(db_models.Ecosystem).filter(
                #     db_models.Ecosystem.id == new_acosystem.id
                # )

            else:
                logger.info("Ecosystem alive")
                return await self.handle_ecosystem_evolution(ecosystem_alive, request)
                # db.query(db_models.Ecosystem).filter(
                #     db_models.Ecosystem.id == ecosystem_alive.id
                # )

        except Exception as e:
            # db.close()
            logger.error(f"Error on check evolution: {e}")

    def get_ecosystems_count(self):
        return db.query(func.count(db_models.Ecosystem.id)).scalar()

    def get_alive_ecosystem(self):
        return (
            db.query(db_models.Ecosystem)
            .filter(
                db_models.Ecosystem.born_date != None,
                db_models.Ecosystem.extinction_date == None,
            )
            .first()
        )

    async def handle_new_ecosystem(self, request: models.EvolutionRequest):
        logger.info("Is a new ecosystem possible?")
        if random.random() < config.NEW_ECO_PROB:
            logger.info("Creating new ecosystem...")
            return await self.create_new_ecosystem(request)

    async def handle_ecosystem_evolution(
        self, ecosystem_alive, request: models.EvolutionRequest
    ):
        ecosystem_id = ecosystem_alive.id
        messages = ecosystem_alive.messages
        total_messages = ecosystem_alive.total_messages
        current_ecosystem = ast.literal_eval(ecosystem_alive.ecosystem)
        evolutions = ecosystem_alive.evolutions
        probability = messages * config.PROB_PER_MESSAGE
        if random.random() < probability:
            new_ecosystem, died_by_epidemic = ecosystem.evolution(
                current_ecosystem, evolutions
            )
            logger.info(new_ecosystem)
            ecosystem_died = all(
                all(elem == " " for elem in sublist) for sublist in new_ecosystem
            )
            if ecosystem_died:
                return await self.kill_ecosystem(
                    ecosystem_id,
                    died_by_epidemic,
                    messages,
                    total_messages,
                    request,
                )
            else:
                return await self.evolution(
                    ecosystem_id,
                    total_messages,
                    new_ecosystem,
                    evolutions,
                )
        else:
            ecosystem_alive.messages += 1
            ecosystem_alive.total_messages += 1
            db.merge(ecosystem_alive)
            return "No evolution happened, but ecosystem is still alive.", None, None
            # db.close()

    async def create_new_ecosystem(self, request: models.EvolutionRequest):
        ecosystem = Ecosystem()
        message = request.message
        user = request.user
        logger.info("Creating new ecosystem...")
        msg = msgs.ECOSYSTEM_CREATED
        logger.info(msg)
        new_ecosystem = ecosystem.new_ecosystem(user + str(message))
        logger.info(new_ecosystem)
        ecosystem_to_add = db_models.Ecosystem(
            ecosystem=str(new_ecosystem),
            messages=0,
            total_messages=0,
            evolutions=0,
            born_date=utils.get_date(),
            creator=user,
        )
        logger.info("Saving new ecosystem to database...")
        db.merge(ecosystem_to_add)
        logger.info("New ecosystem saved to database")
        db.commit()
        msg = await utils.prepare_message(
            msg,
            prompt=prompts.ECOSYSTEM_BORN,
        )
        updated_ecosystem = (
            db.query(db_models.Ecosystem)
            .filter(db_models.Ecosystem.id == ecosystem_to_add.id)
            .first()
        )

        # ecosystem = await utils.prepare_message(
        #     ecosystem.format_ecosystem(new_ecosystem)
        # )
        # db.close()
        return msg, new_ecosystem, updated_ecosystem

    async def kill_ecosystem(
        self,
        ecosystem_id,
        died_by_epidemic,
        messages,
        total_messages,
        request: models.EvolutionRequest,
    ):
        ecosystem = Ecosystem()
        prompt = prompts.ECOSYSTEM_DIE
        if died_by_epidemic:
            msg = msgs.EPIDEMIC
            prompt = prompts.ECOSYSTEM_DIE_EPIDEMIC
        else:
            msg = msgs.ECOSYSTEM_DIED
        logger.info(msg)
        died_ecosystem = db_models.Ecosystem(
            id=ecosystem_id,
            messages=messages + 1,
            total_messages=total_messages + 1,
            extinction_date=utils.get_date(),
            killer=request.user,
        )
        db.merge(died_ecosystem)
        db.commit()
        msg = await utils.prepare_message(
            msg,
            prompt=prompt,
        )
        updated_ecosystem = (
            db.query(db_models.Ecosystem)
            .filter(db_models.Ecosystem.id == ecosystem_id)
            .first()
        )
        # ecosystem = await utils.prepare_message(
        #     ecosystem.format_ecosystem(ecosystem.died_ecosystem())
        # )
        # db.close()
        return msg, ecosystem.died_ecosystem(), updated_ecosystem

    async def evolution(self, ecosystem_id, total_messages, new_ecosystem, evolutions):
        # ecosystem = Ecosystem()
        msg = msgs.EVOLUTION
        logger.info(msg)
        evolutions += 1
        ecosystem_alive = db_models.Ecosystem(
            id=ecosystem_id,
            ecosystem=str(new_ecosystem),
            messages=0,
            total_messages=total_messages + 1,
            evolutions=evolutions,
        )

        db.merge(ecosystem_alive)
        db.commit()
        msg = await utils.prepare_message(
            msg,
            prompt=prompts.ECOSYSTEM_EVOLUTION,
        )
        updated_ecosystem = (
            db.query(db_models.Ecosystem)
            .filter(db_models.Ecosystem.id == ecosystem_id)
            .first()
        )

        # ecosystem = await utils.prepare_message(
        #     ecosystem.format_ecosystem(new_ecosystem)
        # )
        # db.close()
        return msg, new_ecosystem, updated_ecosystem
