DEFAULT_CONFIG = {'WHITE_CELL': (255, 255, 255),
                  'BLACK_CELL': (128, 128, 128),
                  'HIGHLIGHTED_CELL': (0, 255, 0),
                  'SELECTED_CELL': (0, 0, 255),
                  'WHITE_CHECKER': (255, 0, 0),
                  'BLACK_CHECKER': (32, 32, 32),
                  'KING_CROWN_COLOR': (255, 255, 0),
                  
                  'CHECKER_SIZE_KOEF': 65,
                  'CHECKER_CROWN_KOEF': 30,
                  'CHECKER_SELECTED_KOEF': 130,
                  'FPS': 60,

                  'LOAD_SESSIONS_ON_STARTUP': True,
                  'SAVE_SESSIONS_ON_EXIT': True,
                  'DELETE_SESSION_AFTER_END': False,
                  'READ_CONFIG_ON_STARTUP': True,
                  'SAVE_CONFIG_ON_EXIT': True,

                  'USERNAME': 'Ivan Nikolayevich',
                  'HOST': '',
                  'IP_TO_CONNECT': ''}

AVALIBLE_CONFIG_NAMES = ("WHITE_CELL",
                         "BLACK_CELL",
                         "HIGHLIGHTED_CELL",
                         "SELECTED_CELL",
                         "WHITE_CHECKER",
                         "BLACK_CHECKER",
                         "KING_CROWN_COLOR",
                         
                         "CHECKER_SIZE_KOEF",
                         "CHECKER_CROWN_KOEF",
                         "CHECKER_SELECTED_KOEF",
                         "FPS",
                         
                         "LOAD_SESSIONS_ON_STARTUP",
                         "SAVE_SESSIONS_ON_EXIT",
                         "DELETE_SESSION_AFTER_END",
                         "READ_CONFIG_ON_STARTUP",
                         "SAVE_CONFIG_ON_EXIT")

AVALIBLE_CONFIG_INFO = (("COLORS",),
                        ("COLORS",),
                        ("COLORS",),
                        ("COLORS",),
                        ("COLORS",),
                        ("COLORS",),
                        ("COLORS",),
                        
                        ("NUMBER",),
                        ("NUMBER",),
                        ("NUMBER",),
                        ("NUMBER",),
                        
                        ("FLAG",),
                        ("FLAG",),
                        ("FLAG",),
                        ("FLAG",),
                        ("FLAG",))

CONFIG = {}

def SetConfig(config, bkp_req=True):
    global CONFIG
    config_bkp = {}
    try:
        for key in config:
            if bkp_req: config_bkp[key] = globals()[key]
            globals()[key] = config[key]
    except:
        for key in config_bkp: globals()[key] = config_bkp[key]
        return False
    
    CONFIG = CONFIG | config
    return True

def ReadConfigFromFile():
    if not os.path.isfile(WORKING_DIR + PATH_TO_CONFIG): return "File not found"
    with open(WORKING_DIR + PATH_TO_CONFIG, 'r', encoding="utf-8") as file:
        config = {}
        try: config |= eval(file.read().strip())
        except: return "Invalid config format"
        if not SetConfig(config): return "Failed to set config"
    return ""

def WriteConfigToFile():
    try:
        with open(WORKING_DIR + PATH_TO_CONFIG, 'w', encoding="utf-8") as file: print(CONFIG, file=file)
    except: return "Something went wrong idk"
    return ""

def SetDefaultConfig(): SetConfig(DEFAULT_CONFIG)

SetConfig(DEFAULT_CONFIG, bkp_req=False)
