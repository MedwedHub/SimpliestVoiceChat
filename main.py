import pyaudio
import socket
import threading

HOST = input("Enter host IP")
PORT = int(input("Enter host port"))
ADDRESS = (HOST, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(ADDRESS)



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

vol_stream = a.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                output_device_index=output_index,
                frames_per_buffer=CHUNK)

mic_stream = a.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=input_index,
                frames_per_buffer=CHUNK)


def acc(stream, server):
    while True:
        data = stream.read(CHUNK)
        server.send(data)

threading.Thread(target=acc, args=(mic_stream, server)).start()

while True:
    inet_data = server.recv(CHUNK)
    vol_stream.write(inet_data)
