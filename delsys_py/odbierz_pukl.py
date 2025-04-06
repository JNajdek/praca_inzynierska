import socket
import socket
import select
import struct
import numpy as np
import pickle
from libemg.shared_memory_manager import SharedMemoryManager
from multiprocessing import Process, Event, Lock

def cmd(command):
    return bytes("{}{}".format(command, '\r\n\r\n'),
                 encoding='ascii')
def validate(response):
    s = str(response)
    if 'OK' not in s:
        print("warning: TrignoDaq command failed: {}".format(s))

comm_socket = socket.create_connection(
            ('localhost', 50040), 10)
comm_socket.recv(1024)

# create the data socket
data_socket = socket.create_connection(
    ('localhost', 50043), 10)
data_socket.setblocking(1)

# create the aux data socket
aux_socket = socket.create_connection(
    ('localhost', 50044), 10)
aux_socket.setblocking(1)

rd_sockets = [data_socket, aux_socket]

comm_socket.send(cmd('START'))
resp = comm_socket.recv(128)
validate(resp)
print('yaaaaay')

emg = True
imu = True
BYTES_PER_CHANNEL = 4
min_recv_size = 16 * BYTES_PER_CHANNEL
emg_handlers = []
imu_handlers = []
channel_list = [0,1,2,3,4,5,6,7]
min_aux_recv_size = (9 * 16) * BYTES_PER_CHANNEL

while True:
    try:
        ready_sockets, _, _ = select.select(rd_sockets, [], [])

        for sock in ready_sockets:
            if (emg and sock == data_socket):
                packet = sock.recv(min_recv_size)
                print(packet)
                data = np.asarray(struct.unpack('<' + 'f' * 16, packet))
                print('2')
                data = data[channel_list]
                if len(data.shape) == 1:
                    data = data[:, None]
                for e in emg_handlers:
                    e(data)
            elif (imu and sock == aux_socket):
                packet = sock.recv(min_aux_recv_size)
                data = np.asarray(struct.unpack('<' + 'f' * 16 * 9, packet))
                assert np.any(data != 0), "IMU not currently working"
                if len(data.shape) == 1:
                    data = data.reshape((-1, 9))[channel_list, :]
                    data = data.reshape(-1)[None, :]
                else:
                    data = np.reshape(data, (data.shape[0], 9, -1))
                    data = data[:, channel_list, :]
                    data = np.reshape(data, (data.shape[0], -1))
                for i in imu_handlers:
                    i(data)
        A = 1

    except Exception as e:
        print("Error Occurred: " + str(e))
        continue