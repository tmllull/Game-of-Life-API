from openai import AzureOpenAI, OpenAI

# from src.clients.azure_openai import AzureOAI
# from src.clients.openai import OpenAI
from src.utils.logger import LogManager

from src.utils import prompts as prompts
from src.config.config import Config

config = Config()
logger = LogManager()


class AIController:
    def __init__(self):
        if config.AI_SERVICE is None or (
            config.AI_SERVICE != "openai" and config.AI_SERVICE != "azure"
        ):
            logger.info("AI_SERVICE is not set")
            self.has_service = False
        else:
            self.has_service = True
            if config.AI_SERVICE == "openai":
                logger.info("AI_SERVICE is set to OpenAI")
                self._client = OpenAI(api_key=config.OPENAI_API_KEY)
                self._MODEL = config.OPENAI_MODEL
            elif config.AI_SERVICE == "azure":
                logger.info("AI_SERVICE is set to Azure OpenAI")
                self._client = AzureOpenAI(
                    api_key=config.AZURE_API_KEY,
                    api_version=config.AZURE_API_VERSION,
                    azure_endpoint=config.AZURE_API_ENDPOINT,
                )
                self._MODEL = config.AZURE_MODEL_NAME

    async def generate_text(self, prompt) -> str:
        messages = [
            {
                "role": "system",
                "content": prompts.INSTRUCTION,
            },
            {"role": "user", "content": prompt},
        ]
        response = self._client.chat.completions.create(
            model=self._MODEL,
            messages=messages,
        )
        logger.info(response.usage.total_tokens)
        return response.choices[0].message.content
        # if config.AI_SERVICE == "openai":
        #     logger.info("Generating text using OpenAI...")
        #     return open_ai.generate_text(pre_prompt, prompt)
        # elif config.AI_SERVICE == "azure":
        #     logger.info("Generating text using Azure OpenAI...")
        #     return azure_openai.generate_text(pre_prompt, prompt)
        # else:
        #     logger.info("AI_SERVICE is not set")
        #     logger.info(config.AI_SERVICE)
