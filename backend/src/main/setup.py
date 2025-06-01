from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.src.config import config, CONFIG_FILE
from backend.src.database import test_db_connection
from typing import Optional

router = APIRouter(prefix="/setup", tags=["Setup"])


class SetupConfig(BaseModel):
    MONGO_URI: str
    MONGO_DB: str
    BINDING_KEY: str
    OLLAMA: bool
    OLLAMA_HOST: Optional[str] = None


@router.post("/")
async def setup(setup_config: SetupConfig):
    """
    Initial setup endpoint to configure the application.
    """
    # Test MongoDB connection
    if not await test_db_connection(setup_config.MONGO_URI, setup_config.MONGO_DB):
        raise HTTPException(status_code=400, detail="Invalid MongoDB configuration")

    # Configure sections
    if not config.has_section('Global'):
        config.add_section('Global')
    if not config.has_section('MONGO'):
        config.add_section('MONGO')
    if not config.has_section('Security'):
        config.add_section('Security')
    if not config.has_section('Ollama'):
        config.add_section('Ollama')

    # Set configuration values
    config['Global']['FirstSetup'] = 'False'
    config['MONGO']['MONGO_URI'] = f'"{setup_config.MONGO_URI}"'
    config['MONGO']['MONGO_DB'] = f'"{setup_config.MONGO_DB}"'
    config['Security']['BINDING_KEY'] = f'"{setup_config.BINDING_KEY}"'
    config['Ollama']['enabled'] = str(setup_config.OLLAMA)

    if setup_config.OLLAMA and setup_config.OLLAMA_HOST:
        config['Ollama']['host'] = f'"{setup_config.OLLAMA_HOST}"'

    # Save configuration to file
    with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

    return {"status": "success", "message": "Setup completed successfully"}
