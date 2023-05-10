# ATTENTION: this code doesn't respect declaration sequence
import socket
import random

HOST = "192.168.31.209" #"192.168.1.113"
IP_TO_CONNECT = "192.168.31.44" #"192.168.1.152"

PORTS_R = (2000, 2001)
PORTS_S = (3000, 3001)
PORT_R = PORTS_R[0]
PORT_S = PORTS_S[0]

SOCKET_R = socket.socket()
SOCKET_S = socket.socket()
try: SOCKET_R.bind((HOST, PORT_R))
except: globals()["PORT_R"] = PORTS_R[1]; SOCKET_R.bind((HOST, PORT_R)); print("I USED ADDITIONAL R PORT")
try: SOCKET_S.bind((HOST, PORT_S))
except: globals()["PORT_S"] = PORTS_S[1]; SOCKET_S.bind((HOST, PORT_S)); print("I USED ADDITIONAL S PORT")

#print("I AM USING", PORT_R, "AS R AND", PORT_S, "AS S")

SOCKET_R.listen(1)
IS_CONNECTED = False

def EstConnection(is_opening):
    global SOCKET_R
    global SOCKET_S
    global IP_TO_CONNECT
    if is_opening:
        SOCKET_R.settimeout(20)
        #print("OPENING", (HOST, PORT_R))
        SOCKET_R, IP_TO_CONNECT = SOCKET_R.accept()
        #print(IP_TO_CONNECT, "WAS CONNECTED")
        IP_TO_CONNECT = IP_TO_CONNECT[0]
        SOCKET_R.settimeout(5)
    else:
        SOCKET_S.settimeout(1)
        try:
            #print("TRYING TO CONNECT TO", (IP_TO_CONNECT, PORTS_R[0]))
            SOCKET_S.connect((IP_TO_CONNECT, PORTS_R[0]))
        except:
            #print("FAILED, TRYING", (IP_TO_CONNECT, PORTS_R[1]))
            SOCKET_S = socket.socket()
            SOCKET_S.bind((HOST, PORT_S))
            SOCKET_S.settimeout(1)
            SOCKET_S.connect((IP_TO_CONNECT, PORTS_R[1]))
        #print("I CONNECTED")
        SOCKET_S.settimeout(10)

def Connect(open_first):
    global STATE, PLAYER_COLOR, CUR_COLOR
    EstConnection(open_first)
    EstConnection(not open_first)
    print("Connection Established")
    globals()["IS_CONNECTED"] = True
    
    if open_first:
        SOCKET_S.send((STATE + globals()["PLAYER_COLOR"] + CUR_COLOR).encode())
    else:
        data = SOCKET_R.recv(100).decode()
        STATE = data[:64]
        PLAYER_COLOR = data[64]
        ChangePlayerColor()
        CUR_COLOR = data[65]
    globals()["GAME_MODE"] = "MULTIPLAYER"
    RunGame()
    print(PLAYER_COLOR)
    
def Disconnect(send=False):
    if send: SOCKET_S.send("DISCONNECT".encode())
    globals()["IS_CONNECTED"] = False
    SetMenu("MAIN")

def OtherPlayerHandler():
    SOCKET_R.settimeout(1)
    try: msg = SOCKET_R.recv(1024).decode()
    except: return
    print("I GOT", msg)
    if msg == "DISCONNECT": globals()["IS_CONNECTED"] = False
    elif msg.startswith("MOVE"): Move(int(msg.split()[1]))
    elif msg.startswith("SELECT"): SelectChecker(int(msg.split()[1]), show=False)
        
