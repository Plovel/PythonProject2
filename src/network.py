# ATTENTION: this code doesn't respect declaration sequence
import socket
import random
import time

HOST = ""
IP_TO_CONNECT = "127.0.0.1"

PORTS_R = (2000, 2001)
PORTS_S = (3000, 3001)
if 0: PORTS_R, PORTS_S = PORTS_R[::-1], PORTS_S[::-1]
RESERVED_PORT = 8237

PORT_R = None
PORT_S = None

SOCKET_R = socket.socket()
SOCKET_S = socket.socket()
PORT_R_FLAG = False
PORT_S_FLAG = False

def Disconnect(send=True):
    global PORT_R_FLAG, PORT_S_FLAG
    if send:
        try: SOCKET_S.settimeout(0.1); SOCKET_S.send("DISCONNECT".encode())
        except: pass
    globals()["IS_CONNECTED"] = False
    globals()["GAME_MODE"] = "BOT"
    SOCKET_R.close()
    SOCKET_S.close()
    PORT_R_FLAG, PORT_S_FLAG = False, False

def ExitMultiplayer(txt, menu="MAIN"):
    Disconnect(True)
    if txt: ShowText(txt, txt_col=ORANGE)
    if not menu is None: SetMenu(menu)

SOCKET_CHECK_REQ = False
def CheckSocket(host, port):
    if not SOCKET_CHECK_REQ: return False
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    res = True
    for i in range(10):
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if DebOut: print("CHECKING", (host, port), skt.connect_ex((host, port)) == 0)
        skt.close()
    try: sock.connect((host, port))
    except: sock.close(); res = False
    sock.close()
    if res: print((host, port), "IS BUSY")
    else: print((host, port), "IS FREE")
    return res

def SetUpSockets():
    global SOCKET_R, SOCKET_S, PORT_R_FLAG, PORT_S_FLAG, PORT_R, PORT_S

    if not PORT_R_FLAG:
        SOCKET_R.close()
        SOCKET_R = socket.socket()
        SOCKET_R.settimeout(0.1)
        for port in PORTS_R:
            if CheckSocket(HOST, port):
                if DebOut: print(res, f"R PORT {port} IS BUSY")
                continue
            SOCKET_R.bind((HOST, port))
            PORT_R = port; SOCKET_R.listen(1)
            if DebOut: print(f"I USED {PORT_R} AS R PORT", HOST)
            PORT_R_FLAG = True
            break         
        else: return "Failed to find free R port"
    if not PORT_S_FLAG:
        SOCKET_S.close()
        SOCKET_S = socket.socket()
        SOCKET_S.settimeout(0.1)
        for port in PORTS_S:
            try: SOCKET_S.bind((HOST, port))
            except: continue
            PORT_S = port
            if DebOut: print(f"I USED {PORT_S} AS S PORT", HOST)
            PORT_S_FLAG = True
            break
        else: return "Failed to find free S port"
    return ""

def EstConnection(is_opening):
    global SOCKET_R
    global SOCKET_S
    global IP_TO_CONNECT
    DebOut = True
    if is_opening:
        try:
            SOCKET_R.settimeout(2)
            if DebOut: print("YOU CAN CONNECT TO ME WITH", (HOST, PORT_R))
            SOCKET_R, IP_TO_CONNECT = SOCKET_R.accept()
            IP_TO_CONNECT = IP_TO_CONNECT[0]
        except: return "Player did not connect"
    else:
        for port in PORTS_R:
            SOCKET_R.settimeout(0.5)
            if PORT_R == port: continue
            if DebOut and random.randint(0, 1000) % 50 == 0:
                if DebOut: print("TRYING TO CONNECT TO", (IP_TO_CONNECT, port))
            try: SOCKET_S.connect((IP_TO_CONNECT, port))
            except: continue
            if DebOut: print("I CONNECTED TO", PORT_R, port)
            break
        else: return "No avalible games"
    return ""

IS_OPENING_GAME = None
timer_for_opening = time.time()
time_out_to_recieve = 10
def Connect():
    global STATE, PLAYER_COLOR, CUR_COLOR
    cur_timer = time.time() - timer_for_opening
    if time_out_to_recieve <= cur_timer:
        message = ("No avalible games", "No one connected")[IS_OPENING_GAME]
        menu = ["SESSIONS", "SESSIONS"][IS_OPENING_GAME]
        ExitMultiplayer(message, menu=menu)
        return
    BUTTONS[1].text = str(round(time_out_to_recieve - cur_timer))
    BUTTONS[1].draw()
    pygame.display.flip()
    
    res = SetUpSockets()
    if res:
        ExitMultiplayer("Failed to open ports\nReason: " + res, menu=None)
        return
    
    res += EstConnection(IS_OPENING_GAME)
    if res: return
    
    res += EstConnection(not IS_OPENING_GAME)
    if res: return
    
    if DebOut: print("Connection Established")
    globals()["IS_CONNECTED"] = True
    
    if IS_OPENING_GAME:
        SOCKET_S.send((STATE + PLAYER_COLOR + CUR_COLOR).encode())
    else:
        try:
            SOCKET_R.settimeout(0.5)
            data = SOCKET_R.recv(100).decode()
        except:
            ExitMultiplayer("Remote app did not\nsend session data",
                            menu="SESSIONS")
            return
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
        if DebOut: print("CONNECTION CHECK FAILED")
        globals()["is_check_req"] = False
        ExitMultiplayer("Player app did not response"); return
    if random.randint(1, 10000) % 10 == 0:
        try: SOCKET_S.settimeout(0.01); SOCKET_S.send("CHECK ".encode())
        except: ExitMultiplayer("Bad connection to player"); return
        globals()["is_check_req"] = True
        globals()["req_time"] = time.time()
    #checking connection
    
    try: SOCKET_R.settimeout(0.1)
    except: ExitMultiplayer("Recieve socket does not work"); return
    messages = ''
    try: messages += SOCKET_R.recv(1024).decode()
    except:
        ExitMultiplayer("Recieve socket doesnt work\nor timeout")
        return
    messages = messages.split()
    for message in messages:
        if message == "DISCONNECT": ExitMultiplayer("Other player exited game"); return
        elif message.startswith("MOVE"): Move(int(message[5:]))
        elif message.startswith("SELECT"): SelectChecker(int(message[7:]), show=False)
        elif message == ("CHECK"):
            try: SOCKET_S.send("OK ".encode())
            except: ExitMultiplayer("Unknown socket error", menu="SESSIONS")
        elif message == ("OK"): globals()["is_check_req"] = False

