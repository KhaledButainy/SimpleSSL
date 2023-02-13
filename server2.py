import secrets
import socket
import pickle
import hashlib
from Crypto import *
from Crypto.Cipher import AES
from tttgame import *


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #Server IPv4 address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
BLOCK_SIZE = 16 #bytes
#Server's public and private key, and Client's public key
N = "Put N value here"
e = 211
PRIVATE_KEY = "Put your private key here, should be different than server.py"
PUBLIC_KEY = (N, e)
CLIENT_PUBLIC_K = ("Client public key", "'e' of the client")
#Parameters to generate a shared symmetric key (B and G^B mod M are inside handle_client())
M = "M value"
G = 2
#Server's RB and ID
RB = str(secrets.randbits(BLOCK_SIZE*16))
SERVER_ID = "SERVER"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(ADDR)

def handle_client(conn, addr, g):
    print(f"[NEW CONNECTION] {addr} connected\n")
    B = secrets.randbits(BLOCK_SIZE*128)
    GBmodM = str(pow(G, B, M))

    #----------Start of Authentication Protocol----------
    #Step 1 (Recv RA, G^A mod M)
    RA_len = conn.recv(2).decode(FORMAT)
    RA_len = int(RA_len)
    RA = conn.recv(RA_len).decode(FORMAT)
    GAmodM_len = conn.recv(3).decode(FORMAT)
    GAmodM_len = int(GAmodM_len)
    GAmodM = conn.recv(GAmodM_len).decode(FORMAT)

    print(f"B:\n{B}\n")

    #Step 2 (Send RB, G^B mod M, SB)
    GABmodM = str(pow(int(GAmodM), B, M)) #calculate the session key
    B = 0 #destroy B
    CLIENT_ID = "CLIENT"
    H_content = (CLIENT_ID + SERVER_ID + RA + RB + GAmodM + GBmodM + GABmodM).encode(FORMAT)
    H = hashlib.sha256(H_content)
    H = H.digest()
    SB = "0x" + H.hex() + SERVER_ID.encode(FORMAT).hex()
    SB = int(SB, 0)
    SB_enc = str(pow(SB, PRIVATE_KEY, N))
    conn.send(str(len(RB)).encode(FORMAT))
    conn.send(RB.encode(FORMAT))
    conn.send(str(len(GBmodM)).encode(FORMAT))
    conn.send(GBmodM.encode(FORMAT))
    conn.send(str(len(SB_enc)).encode(FORMAT))
    conn.send(SB_enc.encode(FORMAT))
    checkIfAuthenticated = conn.recv(1).decode(FORMAT)
    #after sending RB, G^B mod M, SB. Check if client authenticated server
    if checkIfAuthenticated == "0":
        print("YOU ARE NOT AUTHENTICATED TO CLIENT\n")
        KEY = 0 #destroy the session key
        conn.close()
        exit(0)
    print("YOU ARE AUTHENTICATED TO CLIENT\n")

    KEY = hashlib.sha256(GABmodM.encode(FORMAT))
    KEY = bytes.fromhex(KEY.digest().hex())

    #step 3 (Recv E(CLIENT_ID, SA, K))
    IV_len = conn.recv(2).decode(FORMAT)
    IV_len = (int(IV_len)+1)*2 
    IV = conn.recv(IV_len) #reveive the Initialization Vector
    step3_msg_len = conn.recv(HEADER).decode(FORMAT)
    step3_msg_len = int(step3_msg_len)
    step3_msg = conn.recv(step3_msg_len)
    aes_dec = AES.new(KEY, AES.MODE_CBC, IV)
    step3_msg = aes_dec.decrypt(step3_msg)

    #End of Step 3 (Verify the signature and authenticate the Client)
    SA = str(step3_msg).lstrip("b'").rstrip("'").rstrip()[len(CLIENT_ID):]
    SA = int(SA, 0)
    SA = pow(SA, CLIENT_PUBLIC_K[1], CLIENT_PUBLIC_K[0])
    SA = hex(SA)
    SA = SA.lstrip("'0x").rstrip("'")
    if (len(SA)%2!=0): SA = SA + '0'
    SA = bytes.fromhex(SA)
    full_sa = str(SA).lstrip("b'").rstrip("'")
    server_h = str(H).lstrip("b'").rstrip("'")
    #if the result of H is inside SA and its index is 0, the client will be authenticated
    if (full_sa.find(server_h) == 0):
        print("CLIENT IS AUTHENTICATED TO YOU\n")
        conn.send("1".encode(FORMAT))
    else:
        print("CLIENT IS NOT AUTHENTICATED TO YOU\n")
        conn.send("0".encode(FORMAT))
        KEY = 0 #destroy the session key
        conn.close()
        exit(0)

    print(f"IV:\n{IV.hex()}\n")
    print(f"SESSION KEY:\n{KEY.hex()}\n") 
    print(f"RA:\n{RA}\n")
    print(f"RB:\n{RB}\n")
    #----------End of Authentication Protocol----------


    while True:
        
        #Server plays
        g.play(g.getTurn())                         #play and update the board
        smsg = pickle.dumps(g)                      #pickle the object
        if(len(smsg)%BLOCK_SIZE != 0):
            smsg += b' ' * (BLOCK_SIZE - (len(smsg)%BLOCK_SIZE))
        smsg_len = len(smsg)                        #define the the object length
        send_len = str(smsg_len).encode(FORMAT)     
        conn.send(send_len)                         #send the object length first
        aes_enc = AES.new(KEY, AES.MODE_CBC, IV)
        print("\nbefore encryption (pickled object):\n"+ smsg.hex())
        smsg = aes_enc.encrypt(smsg)                #encrypting
        print("\nsent encrypted msg:\n"+ smsg.hex())
        conn.send(smsg)                             #send the pickled object encrypted
        if g.win or g.tie:                          #if Server won or its a tie, close the connection
            break
        
        #Server receives and updates his board
        recv_len = conn.recv(HEADER).decode(FORMAT) #receive the object length
        recv_len = int(recv_len)
        recv_msg = conn.recv(recv_len)              #receive the encrypted pickled object
        print("\nrecv encrypted msg:\n"+ recv_msg.hex())
        aes_dec = AES.new(KEY, AES.MODE_CBC, IV)
        recv_msg = aes_dec.decrypt(recv_msg)        #decrypting
        print("\nafter decryption (pickled object):\n"+ recv_msg.hex())
        rmsg = pickle.loads(recv_msg)               #unpickle the object
        print("\nO played:")
        rmsg.printBoard(rmsg.getBoard())            #print the board
        g = rmsg
        if g.win:
            g.setTurn('O')                          #if Client Won, print the result
            g.printWinner(g.tie)
            break
        elif g.tie:                                 #else if the result is tie, print the result
            g.printWinner(g.tie)
            break
    
    KEY = 0 #destroy the session key
    conn.close()
    exit(0)
         

def start():
    server.listen(1)                                #listening, the number of connections is limited to (1)
    b = {'7': ' ' , '8': ' ' , '9': ' ' ,
         '4': ' ' , '5': ' ' , '6': ' ' ,
         '1': ' ' , '2': ' ' , '3': ' ' }
    t = 'X'
    g = tttgame(t, b, 0, 0)                         #initializing the game board
    g.printBoard(g.getBoard())
    print(f"[LISTENING] server is listening on {SERVER}") #print the Server IPv4 address
    while True:
        conn, addr = server.accept()                #accept connection requests
        handle_client(conn, addr, g)                



print("[STARTING] server is starting...")
start()
