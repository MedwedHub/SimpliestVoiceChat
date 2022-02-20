import pyaudio
import socket
import threading

class Peer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_to_host(self):
        self.server.bind((self.ip, self.port))
        self.server.listen(1)

        self.initialize()

    def connect(self):
        self.server.connect((self.ip, self.port))
        print("Connection established!")
        self.initialize(is_host=False)

    def initialize(self, is_host=True):
        a = pyaudio.PyAudio()

        for i in range(a.get_device_count()):
            print(i, a.get_device_info_by_index(i)['name'])


        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        print()
        input_index = int(input('Enter microphone index '))
        output_index = int(input('Enter speaker index '))

        self.vol_stream = a.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        output_device_index=output_index,
                        frames_per_buffer=CHUNK)

        self.mic_stream = a.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=input_index,
                        frames_per_buffer=CHUNK)


        if is_host:
            self.peer, _ = self.server.accept()
            print("Connection established!", self.peer)
        else:
            self.peer = self.server

        threading.Thread(target=self.transmit, args=(self.peer, CHUNK)).start()
        self.receive(self.peer, CHUNK)

    def transmit(self, peer, chunk):
        while True:
            data = self.mic_stream.read(chunk)
            peer.send(data)

    def receive(self, peer, chunk):
        while True:
            data = peer.recv(chunk)
            self.vol_stream.write(data)


if __name__ == '__main__':

    if input("Are you host? y/n\n") == "y":
        PORT = int(input("Enter available port\n"))
        server = Peer('', PORT)
        server.start_to_host()

    else:
        HOST = input("Enter host IP address\n")
        PORT = int(input("Enter host port\n"))
        client = Peer(HOST, PORT)
        client.connect()
