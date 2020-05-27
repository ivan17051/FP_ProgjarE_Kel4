import socket
from _thread import *
from player import Player
import pickle
import os

server = "192.168.1.6"
port = 5555

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
    print("obstacle")

def threaded_client(conn, player):
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
                print("all ready")
                # obstacle script

            conn.sendall(pickle.dumps(reply))
                

        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1