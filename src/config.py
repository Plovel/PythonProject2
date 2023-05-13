PATH_TO_CONFIG = "config.txt"

VarToText = {"WHITE_CELL": "White cell color",
             "BLACK_CELL": "Black cell color",
             "HIGHLIGHTED_CELL": "Avalible cell color",
             "SELECTED_CELL": "Selected cell color",
             "WHITE_CHECKER": "White checker color",
             "BLACK_CHECKER": "Black checker color",
             "KING_CROWN_COLOR": "Crown color",
                        
             "CHECKER_SIZE_KOEF": "Checker size",
             "CHECKER_CROWN_KOEF": "Checker crown size",
             "CHECKER_SELECTED_KOEF": "Selected checker size",
             "FPS": "FPS",
                        
             "LOAD_SESSIONS_ON_STARTUP": "Load sessions when opening",
             "SAVE_SESSIONS_ON_EXIT": "Save sessions when closing",
             "DELETE_SESSION_AFTER_END": "Delete session after game ending",
             "READ_CONFIG_ON_STARTUP": "Read config when opening",
             "SAVE_CONFIG_ON_EXIT": "Save config when closing",

             "USERNAME": "Username",
             "HOST": "Host",
             "IP_TO_CONNECT": "Other player IP address",

             "COMMAND_TO_EXECUTE": "Command to execute"}

TextToVar = {VarToText[key]:key for key in VarToText}



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
                  'IP_TO_CONNECT': '192.168.1.1'}

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

VARS_INFO = {'WHITE_CELL': ("COLORS",),
             'BLACK_CELL': ("COLORS",),
             'HIGHLIGHTED_CELL': ("COLORS",),
             'SELECTED_CELL': ("COLORS",),
             'WHITE_CHECKER': ("COLORS",),
             'BLACK_CHECKER': ("COLORS",),
             'KING_CROWN_COLOR': ("COLORS",),
                        
             'CHECKER_SIZE_KOEF': ("NUMBER",),
             'CHECKER_CROWN_KOEF': ("NUMBER",),
             'CHECKER_SELECTED_KOEF': ("NUMBER",),
             'FPS': ("NUMBER",),
                        
             'LOAD_SESSIONS_ON_STARTUP': ("FLAG",),
             'SAVE_SESSIONS_ON_EXIT': ("FLAG",),
             'DELETE_SESSION_AFTER_END': ("FLAG",),
             'READ_CONFIG_ON_STARTUP': ("FLAG",),
             'SAVE_CONFIG_ON_EXIT': ("FLAG",),

             'USERNAME': ("TEXT",),
             'HOST': ("IP",),
             'IP_TO_CONNECT': ("IP",),

             "COMMAND_TO_EXECUTE": ("TEXT",)}

def GetVar(var):
    if not var in VarToText: var = TextToVar.get(var, "Unknown var")
    return var

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
    if not os.path.isfile(WD + PATH_TO_CONFIG): return "File not found"
    with open(WD + PATH_TO_CONFIG, 'r', encoding="utf-8") as file:
        config = {}
        try: config |= eval(file.read().strip())
        except: return "Invalid config format"
        if not SetConfig(config): return "Failed to set config"
    return ""

def WriteConfigToFile():
    try:
        with open(WD + PATH_TO_CONFIG, 'w', encoding="utf-8") as file:
            print(CONFIG, file=file)
    except: return "Failed to save config"
    return ""

def SetDefaultConfig(): SetConfig(DEFAULT_CONFIG)

SetConfig(DEFAULT_CONFIG, bkp_req=False)
