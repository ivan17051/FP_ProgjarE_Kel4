import socket
from _thread import *
from player import Player
import pickle
import os
import random
import time

# server = "192.168.100.2"
server = socket.gethostbyname(socket.gethostname())
print("Server: " + server)
port = 5555
x = 0
y = 0
w = 0
h = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

# p1 = pygame.image.load(os.getcwd() + '\\Resources\\img\\green.png').convert()
# p2 = pygame.image.load(os.getcwd() + '\\Resources\\img\\blue.png').convert()

players = [Player("Player 1",0,0,100,85,os.getcwd() + '\\Resources\\img\\blue.png'), Player("Player 2",100,100, 100,85, os.getcwd() + '\\Resources\\img\\green.png')]

def generateObstacle():
    global x
    global y
    global w
    global h
    while True:
        x = 1280
        y = random.randrange(0, 720)
        w = random.randrange(100, 200)
        h = random.randrange(100, 200)
        # print(str(x) +","+str(y) +","+str(w) +","+str(h))
        time.sleep(6)

def threaded_client(conn, player):
    global x
    global y
    global w
    global h
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                # print("Received: ", data)
                # print("Sending : ", reply)

            if(players[0].ready and players[1].ready):
                # print("all ready")
                # obstacle script
                if player == 1:
                    players[0].obsRect = (x,y,w,h)
                    print(str(players[0].obsRect[0]) +","+str(players[0].obsRect[1]) +","+str(players[0].obsRect[2]) +","+str(players[0].obsRect[3]))
                    reply = players[0]
                else:
                    players[1].obsRect = (x,y,w,h)
                    print(str(players[1].obsRect[0]) +","+str(players[1].obsRect[1]) +","+str(players[1].obsRect[2]) +","+str(players[1].obsRect[3]))
                    reply = players[1]

                conn.sendall(pickle.dumps(reply))
            else:
                conn.sendall(pickle.dumps(reply))
                

        except:
            break

    print("Lost connection")
    conn.close()

start_new_thread(generateObstacle, ())

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    print(currentPlayer)
    
    if currentPlayer > 1:
        currentPlayer = 0
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1