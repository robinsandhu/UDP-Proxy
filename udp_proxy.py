from threading import Thread
import socket
import importlib
import parser
import os

stop_threads = False

class Proxy2Server(Thread):

    def __init__(self):
        super(Proxy2Server, self).__init__()
        self.game = None
        self.gameAddressPort = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        while True:
            global stop_threads
            if stop_threads:
                break

            byteAddressPair = self.server.recvfrom(4096)
            data = byteAddressPair[0]
            serverAddressPort = byteAddressPair[1]

            try:
                importlib.reload(parser)
                parser.parse(serverAddressPort[0], data, "server")
            except Exception as e:
                print(e)

            # print("<- [{}] {}".format(serverAddressPort[0].center(15, " "), data[:50].hex()))
            if data:
                self.game.sendto(data, self.gameAddressPort)


class Game2Proxy(Thread):

    def __init__(self, port):
        super(Game2Proxy, self).__init__()

        self.server = None
        self.port = port
        self.gameAddressPort = None
        self.serverAddressPort = None
        self.game = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.game.bind(("127.0.0.1", self.port))

    def run(self):
        while True:
            global stop_threads
            if stop_threads:
                break

            byteAddressPair = self.game.recvfrom(4096)
            data = byteAddressPair[0]
            self.gameAddressPort = byteAddressPair[1]

            try:
                importlib.reload(parser)
                parser.parse(self.gameAddressPort[0], data, "client")
            except Exception as e:
                print(e)

            # print("-> [{}] {}".format(self.gameAddressPort[0].center(15, " "), data[:50].hex()))
            if data:
                self.server.sendto(data, self.serverAddressPort)


class Proxy(Thread):

    def __init__(self, saddr, sport):
        super(Proxy, self).__init__()
        self.saddr = saddr
        self.sport = sport
        
    def run(self):
        while True:
            print("Staring a new connection")
            self.g2p = Game2Proxy(self.sport)
            self.p2s = Proxy2Server()
            
            # Exchanging references to sockets
            self.g2p.server = self.p2s.server
            self.p2s.game = self.g2p.game

            #Setting up serverAddressPort
            self.g2p.serverAddressPort = (self.saddr, self.sport)

            print("Connection Established")

            # starting the threads
            self.g2p.start()
            while self.g2p.gameAddressPort == None:
                continue
            self.p2s.gameAddressPort = self.g2p.gameAddressPort
            self.p2s.start()


def main():
    global stop_threads
    # server_addr = input("Server address: ")
    # server_port = int(input("Server Port:"))
    master = Proxy("95.216.217.79", 30000)
    master.start()
    while True:
        # You can add further injection logic here
        try:
            choice = input("CMD: ")
            if choice == "q" or choice == "Q":
                stop_threads = True
                os._exit(0)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()