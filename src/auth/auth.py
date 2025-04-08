from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from src.config.config import Config
from src.utils.logger import LogManager

logger = LogManager()
config = Config()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == config.API_KEY:
        return api_key
    else:
        logger.error("Invalid API key")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
