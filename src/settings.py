import os

#Base Paths
dirname = os.path.dirname(__file__)

ASSETS_PATH = os.path.join(dirname, '../assets')
DATA_PATH = os.path.join(dirname, '../data')

#Paths
LOGICGATE_IMAGE_PATH = os.path.join(ASSETS_PATH, 'logic_gates')
BUTTON_IMAGE_PATH = os.path.join(ASSETS_PATH, 'buttons')
FONT_PATH = os.path.join(ASSETS_PATH, 'fonts/Endless Boss Battle.ttf')

#Configs
GRID_SIZE = 10