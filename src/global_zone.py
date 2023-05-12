#game_info
GAME_MODE = "BOT"

STATE = []

PLAYER_COLOR = 'W'
CUR_COLOR = 'W'
REVERSED_ORIENTATION = False
#game_info

#menu_stuffs
APP_STATE = "MENU MAIN"
BUTTONS = []
KEYS_TO_NUMBERS = {pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4}
#menu_stuffs

#config
REBUILD_AND_RUN_ON_EXITING = False
#config

def RUN_COMMAND(command):
    print("executed " + command)
    try: os.popen(command)
    except: return False
    return True

RUNNUNG = True
def ExitApp():
    global RUNNUNG
    if REBUILD_AND_RUN_ON_EXITING: RUN_COMMAND(WORKING_DIR + "../run.sh")
    RUNNUNG = False
