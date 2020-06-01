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

newGame = True

x = 0
y = 0
y2 = 0
w = 0
h = 0

emot = 0

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
    global y2
    global w
    global h
    displayWidth = 1280
    displayHeight = 720
    while True:
        x = displayWidth
        y = random.randrange(displayHeight-300, displayHeight-100)
        y2 = random.randrange(0-400, 0-100)
        w = 100 #random.randrange(100, 200)
        h = 500 #random.randrange(100, 300)
        # print(str(x) +","+str(y) +","+str(w) +","+str(h))
        time.sleep(6)
            

def threaded_client(conn, player):
    global x
    global y
    global y2
    global w
    global h
    global emot
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
                print("p1: " + str(players[0].dead))
                print("p2: " + str(players[1].dead))
                # if(players[0].dead == True or players[1].dead == True):
                #     players[0].game = False 
                #     players[1].game = False
                if player == 1:
                    players[0].obsRect = (x,y,y2,w,h)
                    # print(str(players[0].obsRect[0]) +","+str(players[0].obsRect[1]) +","+str(players[0].obsRect[2]) +","+str(players[0].obsRect[3])+","+str(players[0].obsRect[4]))
                    reply = players[0]
                else:
                    players[1].obsRect = (x,y,y2,w,h)
                    # print(str(players[1].obsRect[0]) +","+str(players[1].obsRect[1]) +","+str(players[1].obsRect[2]) +","+str(players[1].obsRect[3])+","+str(players[1].obsRect[4]))
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
    # global players

    conn, addr = s.accept()
    print("Connected to:", addr)
    print(currentPlayer)
    
    if currentPlayer > 1:
        currentPlayer = 0
        players = [Player("Player 1",0,0,100,85,os.getcwd() + '\\Resources\\img\\blue.png'), Player("Player 2",100,100, 100,85, os.getcwd() + '\\Resources\\img\\green.png')]
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1