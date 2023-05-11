# ATTENTION: this code doesn't respect declaration sequence
import socket
import random
import time

HOST = "127.0.0.1"
IP_TO_CONNECT = "127.0.0.1"

PORTS_R = (2000, 2001)
PORTS_S = (3000, 3001)
PORT_R = PORTS_R[0]
PORT_S = PORTS_S[0]

SOCKET_R = socket.socket()
SOCKET_S = socket.socket()
IS_CONNECTED = False

def Disconnect(send=True):
    if send:
        try: SOCKET_S.send("DISCONNECT".encode())
        except: pass
    globals()["IS_CONNECTED"] = False
    globals()["GAME_MODE"] = "BOT"
    SOCKET_R.close()
    SOCKET_S.close()

def ExitMultiplayer(txt, menu="MAIN"):
    Disconnect(True)
    if txt: ShowText(txt)
    if not menu is None: SetMenu(menu)

def SetUpSockets():
    global SOCKET_R, SOCKET_S
    SOCKET_R.close()
    SOCKET_S.close()
    SOCKET_R = socket.socket()
    SOCKET_S = socket.socket()
    try:
        if True:
            try: SOCKET_R.bind((HOST, PORT_R))
            except:
                try: globals()["PORT_R"] = PORTS_R[1]; SOCKET_R.bind((HOST, PORT_R)); 
                except: return "Failed to set recieve socket"
        if True:
            try: SOCKET_S.bind((HOST, PORT_S))
            except:
                try: globals()["PORT_S"] = PORTS_S[1]; SOCKET_S.bind((HOST, PORT_S)); 
                except: return "Faied to set sending socket" 
    except: return "Unknown reason"
    SOCKET_R.listen(1)
    print(f"I USED {PORT_R} AS R PORT")
    print(f"I USED {PORT_S} AS S PORT")
    return ""

#print("I AM USING", PORT_R, "AS R AND", PORT_S, "AS S")

def EstConnection(is_opening):
    global SOCKET_R
    global SOCKET_S
    global IP_TO_CONNECT
    if is_opening:
        try:
            SOCKET_R.settimeout(0.1)
            SOCKET_R, IP_TO_CONNECT = SOCKET_R.accept()
            IP_TO_CONNECT = IP_TO_CONNECT[0]
        except: return "Player did not connect"
    else:
        try:
            try:
                SOCKET_S.settimeout(1)
                if PORTS_R != PORTS_R[0]: SOCKET_S.connect((IP_TO_CONNECT, PORTS_R[0]))
                else: raise Exception("I dont want to connect to my port")
            except:
                SOCKET_S = socket.socket()
                SOCKET_S.bind((HOST, PORT_S))
                SOCKET_S.settimeout(1)
                SOCKET_S.connect((IP_TO_CONNECT, PORTS_R[1]))
                SOCKET_S.settimeout(10)
        except: return "Failed to connect to player"
    return ""

IS_OPENING_GAME = None
timer_for_opening = time.time()
time_out_to_recieve = 5
def Connect():
    global STATE, PLAYER_COLOR, CUR_COLOR
    cur_timer = time.time() - timer_for_opening
    if time_out_to_recieve <= cur_timer: ExitMultiplayer(["No avalible games", "No one connected"][IS_OPENING_GAME], menu="SESSIONS"); return
    BUTTONS[1].text = str(round(time_out_to_recieve - cur_timer))
    BUTTONS[1].draw()
    pygame.display.flip()
    
    res = SetUpSockets()
    if res: ExitMultiplayer("Failed to open ports\nReason: " + res, menu=None); return
    
    try: res += EstConnection(IS_OPENING_GAME)
    except: return
    if res: return
    
    try: res += EstConnection(not IS_OPENING_GAME)
    except: return
    if res: return
    
    print("Connection Established")
    globals()["IS_CONNECTED"] = True
    
    if IS_OPENING_GAME:
        SOCKET_S.send((STATE + globals()["PLAYER_COLOR"] + CUR_COLOR).encode())
    else:
        data = SOCKET_R.recv(100).decode()
        STATE = data[:64]
        PLAYER_COLOR = data[64]
        ChangePlayerColor()
        CUR_COLOR = data[65]
    globals()["GAME_MODE"] = "MULTIPLAYER"
    RunGame()

is_check_req = False
req_time = time.time()
req_timeout = 1
def OtherPlayerHandler():
    #checking connection
    if is_check_req and time.time() - req_time > req_timeout:
        print("CONNECTION CHECK FAILED")
        globals()["is_check_req"] = False
        ExitMultiplayer("Player app did not response"); return
    if random.randint(1, 10000) % 10 == 0:
        try: SOCKET_S.settimeout(0.01); SOCKET_S.send("CHECK ".encode())
        except: ExitMultiplayer("Bad connection to player"); return
        #print("I requested check")
        globals()["is_check_req"] = True
        globals()["req_time"] = time.time()
    #checking connection
    
    try: SOCKET_R.settimeout(0.1)
    except: ExitMultiplayer("Recieve socket doesnt work"); return
    messages = ''
    try: messages += SOCKET_R.recv(1024).decode()
    except: pass #ExitMultiplayer("Recieve socket doesnt work\nor timeout"); return
    messages = messages.split()
    #print(messages)
    for message in messages:
        if message == "DISCONNECT": ExitMultiplayer("Other player exited game"); return
        elif message.startswith("MOVE"): Move(int(message[5:]))
        elif message.startswith("SELECT"): SelectChecker(int(message[7:]), show=False)
        elif message == ("CHECK"):
            try: SOCKET_S.send("OK ".encode())
            except: print("wtf")
            #print("I SENT IM CONNECTED")
        elif message == ("OK"): globals()["is_check_req"] = False

