import configparser
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class CasePreservingConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

config = CasePreservingConfigParser()
config_file = Path('config.ini')


# Check if the config file exists and read it
if config_file.exists():
    config.read('config.ini')
else:
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def is_dev():
    return os.getenv('ENV') == 'dev'

# Check if the "Global" section exists, if not, first_setup should be True
if not config.has_section('Global'):
    first_setup = True
else:
    first_setup = config.getboolean('Global', 'FirstSetup', fallback=True)

# Only try to get MongoDB settings if we're not in first_setup
if not first_setup:
    try:
        MONGO_URI = os.getenv('MONGO_URI') or config.get('MONGO', 'MONGO_URI').strip('"')
        MONGO_DB = os.getenv('MONGO_DB') or config.get('MONGO', 'MONGO_DB').strip('"')
    except (configparser.NoSectionError, configparser.NoOptionError):
        # If we can't get the MongoDB settings, we should revert to first_setup
        first_setup = True

if first_setup:
    print("First time setup detected.")
    MONGO_URI = None
    MONGO_DB = None