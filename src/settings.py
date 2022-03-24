import os

#Base Paths
dirname = os.path.dirname(__file__)

ASSETS_PATH = os.path.join(dirname, '../assets')
DATA_PATH = os.path.join(dirname, '../data')

#Paths
LOGICGATE_IMAGE_PATH = os.path.join(ASSETS_PATH, 'logic_gates')
BUTTON_IMAGE_PATH = os.path.join(ASSETS_PATH, 'buttons')
FONT_PATH = os.path.join(ASSETS_PATH, 'fonts/Endless Boss Battle.ttf')
FONT_PATH_TK = os.path.join(ASSETS_PATH, 'fonts/Endless Boss Battle')

GRIDDATA_FILE = os.path.join(DATA_PATH, 'gridData.json')
SCOREDATA_FILE = os.path.join(DATA_PATH, 'scores.json')

#Configs
GRID_SIZE = 10
MAX_CUSTOM_LEVELS = 15

#Game settings
EVALUATE_OUTPUT_ROUNDS = 10