import configparser
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class CasePreservingConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

# Compute the absolute path to config.ini relative to this file
CONFIG_FILE = Path(__file__).parent.parent / 'config.ini'
config = CasePreservingConfigParser()

# Check if the config file exists and read it
try:
    if CONFIG_FILE.exists():
        config.read(CONFIG_FILE, encoding='utf-8')
    else:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
except configparser.Error as e:
    print(f"Config file corrupted, creating new one: {e}")
    CONFIG_FILE.unlink()

def is_dev():
    return os.getenv('ENV') == 'dev' or False

# Check if the "Global" section exists, if not, first_setup should be True
if not config.has_section('Global'):
    first_setup = True
else:
    first_setup = config.getboolean('Global', 'FirstSetup', fallback=True)

def optional_config(section, option, default=None):
    try:
        return config.get(section, option).strip('"')
    except (configparser.NoSectionError, configparser.NoOptionError):
        return default

# Only try to get MongoDB settings if we're not in first_setup
if not first_setup:
    try:
        MONGO_URI = os.getenv('MONGO_URI') or config.get('MONGO', 'MONGO_URI').strip('"')
        MONGO_DB = os.getenv('MONGO_DB') or config.get('MONGO', 'MONGO_DB').strip('"')
        OLLAMA_HOST = config.get('Ollama', 'host').strip('"')
        OLLAMA_HEADERS = optional_config("Ollama", "headers")
    except (configparser.NoSectionError, configparser.NoOptionError):
        # If we can't get the settings, we should revert to first_setup
        first_setup = True

if first_setup:
    print("First time setup detected.")
    MONGO_URI = None
    MONGO_DB = None
    OLLAMA_HOST = None
