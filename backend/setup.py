from fastapi import APIRouter, HTTPException, Response
from models import Setup
from config import first_setup, config
from utils import hash_key
from database import test_db_connection

router = APIRouter(prefix="/setup", tags=["Setup"])

@router.post("/", summary="Starts the setup process")
async def start_setup(setup: Setup):
    if not first_setup:
        raise HTTPException(status_code=400, detail="Setup already completed")

    # MongoDB setup
    config['MONGO'] = {
        'MONGO_URI': setup.MONGO_URI,
        'MONGO_DB': setup.MONGO_DB
    }
    if not await test_db_connection(uri=setup.MONGO_URI, db_name=setup.MONGO_DB):
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")
    if setup.OLLAMA:
        config['Ollama'] = {
            'host': setup.OLLAMA_HOST
        }


    # LAST STEP
    config['Global'] = {
        'FirstSetup': 'False',
        'BINDING_KEY': hash_key(setup.BINDING_KEY)
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    return {"message": "Setup completed successfully."}