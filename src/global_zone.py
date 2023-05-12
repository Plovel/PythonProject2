#game_info
GAME_MODE = "BOT"

STATE = []
PLAYER_COLOR = 'W'
CUR_COLOR = 'W'
#game_info

#menu_stuffs
APP_STATE = "MENU MAIN"
BUTTONS = []
KEYS_TO_NUMBERS = {pygame.K_1:1, pygame.K_2:2, pygame.K_3:3, pygame.K_4:4}
#menu_stuffs

#devconfig
REBUILD_AND_RUN_ON_EXITING = False
DebOut = False
#devconfig

def RUN_COMMAND(command):
    if DebOut: print("executed " + command)
    try: os.popen(command)
    except: return False
    return True

RUNNUNG = True
def ExitApp():
    global RUNNUNG
    if REBUILD_AND_RUN_ON_EXITING:
        RUN_COMMAND(WD + "../install.sh && " + WD + "run.sh")
    RUNNUNG = False
