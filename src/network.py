# ATTENTION: this code doesn't respect declaration sequence
import socket
import random
import time

HOST = ""
IP_TO_CONNECT = "127.0.0.1"

SOCKET_CHECK_REQ = False
SOCKET = socket.socket()
CONNECTED_SOCKET = socket.socket()

PORT = 3527
OTHER_PORT = 4253

REMOTE_PORT = None
RESERVED_PORT = 8237

def Disconnect(send=True):
    global SOCKET, CONNECTED_SOCKET
    if send:
        try: SOCKET_S.settimeout(0.1); SOCKET_S.send("DISCONNECT".encode())
        except: pass
    globals()["GAME_MODE"] = "ONE_PLAYER"
    PutChecker()
    CONNECTED_SOCKET.close()
    CONNECTED_SOCKET = socket.socket()
    #try: SOCKET.shutdown(0)
    #except OSError: pass
    #try: SOCKET.shutdown(1)
    #except OSError: pass

def ExitMultiplayer(txt, menu=None):
    Disconnect(True)
    if txt: ShowText(txt, txt_col=ORANGE)
    if not menu is None: SetMenu(menu)

def SetUpSocket():
    DebOut = False
    skt = socket.socket()
    for port in (PORT, OTHER_PORT):
        try: skt.bind((HOST, port))
        except: pass
        if DebOut: print("I used port", port)
        return skt
    return None
    
def EstConnection(is_opening):
    global CONNECTED_SOCKET, IP_TO_CONNECT, REMOTE_PORT
    DebOut = False
    if is_opening:
        skt = SetUpSocket()
        skt.settimeout(1)
        skt.listen(1)
        try:
            if DebOut: print("YOU CAN CONNECT TO ME WITH", (HOST, PORT))
            CONNECTED_SOCKET, info = skt.accept()
            IP_TO_CONNECT, REMOTE_PORT = info
        except socket.timeout: skt.close(); return "Player did not connect"
        skt.close()
    else:
        timeout = 0.1
        flag = True and (random.randint(0, 1000) % 20 == 0)
        for port in (PORT, OTHER_PORT):
            CONNECTED_SOCKET = socket.socket()
            CONNECTED_SOCKET.settimeout(timeout)
            if DebOut and flag: print("CONNECTING", (IP_TO_CONNECT, port))
            try: CONNECTED_SOCKET.connect((IP_TO_CONNECT, PORT)); return ""
            except: CONNECTED_SOCKET.close()
        else: return "Failed to connect"
    return ""

IS_OPENING_GAME = None
timer_for_opening = time.time()
time_out_to_recieve = 10
def Connect():
    global STATE, PLAYER_COLOR, CUR_COLOR
    cur_timer = time.time() - timer_for_opening
    if time_out_to_recieve <= cur_timer:
        message = ("No avalible games", "No one connected")[IS_OPENING_GAME]
        menu = ["SESSIONS", "GAME"][IS_OPENING_GAME]
        ExitMultiplayer(message, menu=menu)
        return
    BUTTONS[1].text = str(round(time_out_to_recieve - cur_timer))
    BUTTONS[1].draw()
    pygame.display.flip()

    res = EstConnection(IS_OPENING_GAME)
    if res: return
    
    if DebOut: print("Connection Established")
    
    if IS_OPENING_GAME:
        CONNECTED_SOCKET.send((STATE + PLAYER_COLOR + CUR_COLOR).encode())
    else:
        try:
            CONNECTED_SOCKET.settimeout(100)
            data = CONNECTED_SOCKET.recv(100).decode()
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

check_works = False
is_check_req = False
req_time = time.time()
req_timeout = 10
def OtherPlayerHandler():
    #checking connection
    if is_check_req and time.time() - req_time > req_timeout:
        if DebOut: print("CONNECTION CHECK FAILED")
        globals()["is_check_req"] = False
        if check_works: ExitMultiplayer("Player's app did not response"); return
    if random.randint(0, 10000) % 50 == 0:
        try: CONNECTED_SOCKET.settimeout(0.1); CONNECTED_SOCKET.send("CHECK ".encode())
        except: ExitMultiplayer("Bad connection to player"); return
        globals()["is_check_req"] = True
        globals()["req_time"] = time.time()
    #checking connection

    try: CONNECTED_SOCKET.settimeout(0.1)
    except: ExitMultiplayer("Socket is broken"); return
    messages = ''
    try: messages += CONNECTED_SOCKET.recv(1024).decode()
    except socket.timeout: pass
    except: ExitMultiplayer("Other player exited game"); return
    messages = messages.split()
    for message in messages:
        if message == "DISCONNECT": ExitMultiplayer("Other player exited game"); return
        elif message.startswith("MOVE"): Move(int(message[5:])); CheckWinner()
        elif message.startswith("SELECT"):
            SelectChecker(int(message[7:]), show=False)
        elif message == ("CHECK"):
            try: CONNECTED_SOCKET.send("OK ".encode())
            except: ExitMultiplayer("Unknown socket error", menu="SESSIONS")
        elif message == ("OK"): globals()["is_check_req"] = False

