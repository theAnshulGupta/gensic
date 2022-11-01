import warnings
import socket
from time import sleep
import math
from gpiozero import Button
from time import time

#! important: make a file called secret in the same directory and write your IP as a string.
#! if you want to run the Pure Data and Python in the same machine, you may also write 'localhost' 
#! e.g. IP = "192.168.1.1" or IP = "localhost"
from secret import IP

def addtime(times):
    if type(times) != list:
        raise(TypeError)
    t = time()
    if len(times) == 0:
        tdiff = 0  # initial seed
    else:
        tdiff = t - times[-1][0]
    return (t, tdiff)

def averagetimes(times):
    averagetime = sum([row[1] for row in times])/float(len(times))
    bpm = (1.0/(averagetime/60.0))
    return (averagetime, bpm)



class PDSocket:
    """PD-PI Socket"""

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def close(self):
        self.sock.close()

    def send(self, msg):
        pdmsg = ';'.join([f'{k} {v}' for k, v in msg.items()])
        sent = self.sock.sendall(bytes(pdmsg + ';', 'ascii'))
        if sent == 0:
            raise RuntimeError("socket connection broken")

    def receive(self):
        msg = str(self.sock.recv(1024), 'ascii')
        if msg == b'':
            raise RuntimeError("socket connection broken")
        return msg[:-2].split(';\n')


def main(host=IP, port=7000):
    
    times = []

    def got_pressed():
        times.append(addtime(times))
        if len(times) > 1:
            if times[0][1] == 0 or len(times) > 16:
                del times[0]
            (averagetime, bpm) = averagetimes(times)
            bpmValue = math.floor(bpm)
            print(bpm, bpmValue)
            socket.send({'tempo': bpmValue})
            
    
    print(f"> Connecting to '{host}' at port '{port}'")
    socket = PDSocket()
    socket.connect(host, port)
    
    bpin = 26
    button = Button(bpin)

    button.when_pressed = got_pressed

    # ?inputs 
    start = 1  # switch
    emotion = 3  # mood
    dis = 0  # dissonance
    dspToggle = 1  # dsp

    #! killswitch
    #start = 0
    #dsp = 0
    
    values = {'start': start, 'emotion': emotion, 'dis': dis, 'dspToggle': dspToggle}
    
    try:
        print("init values")
        socket.send(values)

        while True:
            sleep(10)
            
        print("done")
    except KeyboardInterrupt:
        print("> Closing socket")
        socket.close()


if __name__ == '__main__':
    main()