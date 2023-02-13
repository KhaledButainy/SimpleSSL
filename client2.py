import secrets
import socket
import pickle
import hashlib
from Crypto import *
from Crypto.Cipher import AES
from tttgame import *

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
SERVER = str(input("Enter the server IP address: ")) #asking the client to enter the server IP address
ADDR = (SERVER, PORT)
BLOCK_SIZE = 16 #bytes
IV = secrets.randbits(BLOCK_SIZE*8)
IV = bytes.fromhex(hex(IV).lstrip("'0x").rstrip("'")) #Initialization Vector
#Client's public and private key, and Server's public key
N = "Put your N value here"
e = 349
PRIVATE_KEY = "Put your private key here, should be different than client.py"
PUBLIC_KEY = (N, e)
SERVER_PUBLIC_K = ("Server public key", "'e' of the server")
#Parameters to generate a shared symmetric key
M = "Put your M value here"
G = 2
A = secrets.randbits(BLOCK_SIZE*128)
GAmodM = str(pow(G, A, M))
#Client's RA, Client and Server IDs 
RA = str(secrets.randbits(BLOCK_SIZE*16))
CLIENT_ID = "CLIENT"
SERVER_ID = "SERVER"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

#----------Start of Authentication Protocol----------
#Step 1 (Send RA, G^A mod M)
client.send(str(len(RA)).encode(FORMAT))
client.send(RA.encode(FORMAT))
client.send(str(len(GAmodM)).encode(FORMAT))
client.send(GAmodM.encode(FORMAT))

#Step 2 (Recv RB, G^B mod M, SB)
RB_len = client.recv(2).decode(FORMAT)
RB_len = int(RB_len)
RB = client.recv(RB_len).decode(FORMAT)
GBmodM_len = client.recv(3).decode(FORMAT)
GBmodM_len = int(GBmodM_len)
GBmodM = client.recv(GBmodM_len).decode(FORMAT)
SB_len = client.recv(4).decode(FORMAT)
SB_len = int(SB_len)
SB = client.recv(SB_len).decode(FORMAT)

print(f"A:\n{A}\n")

#End of Step 2 (Verify the signature and authenticate the Server)
SB = int(SB, 0)
SB = pow(SB, SERVER_PUBLIC_K[1], SERVER_PUBLIC_K[0]) #decryption using the server public key
SB = hex(SB)
SB = SB.lstrip("'0x").rstrip("'")
if (len(SB)%2!=0): SB = SB + '0'
SB = bytes.fromhex(SB)
GABmodM = str(pow(int(GBmodM), A, M)) #calculate the session key
A = 0 #destroy A
H_content = (CLIENT_ID + SERVER_ID + RA + RB + GAmodM + GBmodM + GABmodM).encode(FORMAT)
H = hashlib.sha256(H_content)
H = H.digest()
full_sb = str(SB).lstrip("b'").rstrip("'")
client_h = str(H).lstrip("b'").rstrip("'")
#if the result of H is inside SB and its index is 0, the server will be authenticated
if (full_sb.find(client_h) == 0):
    print("SERVER IS AUTHENTICATED TO YOU\n")
    client.send("1".encode(FORMAT))
else:
    print("SERVER IS NOT AUTHENTICATED TO YOU\n")
    client.send("0".encode(FORMAT))
    KEY = 0 #destroy the session key
    client.close()
    exit(0)

KEY = hashlib.sha256(GABmodM.encode(FORMAT))
KEY = bytes.fromhex(KEY.digest().hex())

#step 3 (Send E(CLIENT_ID, SA, K))
SA = "0x" + H.hex() + CLIENT_ID.encode(FORMAT).hex()
SA = int(SA, 0)
SA_enc = str(pow(SA, PRIVATE_KEY, N))
send_IV_len = str(BLOCK_SIZE).encode(FORMAT)
client.send(send_IV_len) #send the IV and its length to the server
client.send(IV)
step3_msg = (CLIENT_ID + SA_enc).encode(FORMAT)
if(len(step3_msg)%BLOCK_SIZE != 0):
    step3_msg += b' ' * (BLOCK_SIZE - (len(step3_msg)%BLOCK_SIZE))
aes_enc = AES.new(KEY, AES.MODE_CBC, IV)
step3_msg = aes_enc.encrypt(step3_msg)
client.send(str(len(step3_msg)).encode(FORMAT))
client.send(step3_msg)
checkIfAuthenticated = client.recv(1).decode(FORMAT)
#after sending E(CLIENT_ID, SA, K), check if server authenticated client
if checkIfAuthenticated == "0":
    print("YOU ARE NOT AUTHENTICATED TO SERVER\n")
    KEY = 0 #destroy the session key
    client.close()
    exit(0)
print("YOU ARE AUTHENTICATED TO SERVER\n")

print(f"IV:\n{IV.hex()}\n")
print(f"SESSION KEY:\n{KEY.hex()}\n") 
print(f"RA:\n{RA}\n")
print(f"RB:\n{RB}\n")
#----------End of Authentication Protocol----------


while True:
    
    #Client receives and updates his board
    recv_len = client.recv(HEADER).decode(FORMAT) #reveive the object length
    recv_len = int(recv_len)
    recv_msg = client.recv(recv_len)              #reveive the encrypted pickled object
    print("\nrecv encrypted msg:\n"+ recv_msg.hex())
    aes_dec = AES.new(KEY, AES.MODE_CBC, IV)
    recv_msg = aes_dec.decrypt(recv_msg)          #decrypting
    print("\nafter decryption (pickled object):\n"+ recv_msg.hex())
    rmsg = pickle.loads(recv_msg)                 #unpickle the object
    print("\nX played:")
    rmsg.printBoard(rmsg.getBoard())              #print the board
    g = rmsg
    if g.win:
        g.setTurn('X')                            #if the Server won, print the result          
        g.printWinner(g.tie)
        break
    elif g.tie:                                   #else if the result is tie, print the result
        g.printWinner(g.tie)
        break
    
    #Client plays
    g.play(g.getTurn())                           #play and update the board
    smsg = pickle.dumps(g)                        #pickle the object
    if(len(smsg)%BLOCK_SIZE != 0):
        smsg += b' ' * (BLOCK_SIZE - (len(smsg)%BLOCK_SIZE))
    smsg_len = len(smsg)                          #define the object length
    send_len = str(smsg_len).encode(FORMAT)       
    client.send(send_len)                         #send the object length first
    aes_enc = AES.new(KEY, AES.MODE_CBC, IV)
    print("\nbefore encryption (pickled object):\n" + smsg.hex())
    smsg = aes_enc.encrypt(smsg)                  #encrypting
    print("\nsent encrypted msg:\n" + smsg.hex())
    client.send(smsg)                             #send the pickled object encrypted
    if g.win or g.tie:                            #if the Client won or its a tie, close the connection
        break

KEY = 0 #destroy the session key
client.close()  
exit(0)


