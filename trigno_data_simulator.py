import socket
import struct
import numpy as np
import time
import threading
import multiprocessing


class TrignoDataSimulator(multiprocessing.Process):
    def __init__(self, host='localhost', data_port=50043, aux_port=50044, cmd_port=50040):
        super().__init__()
        self.host = host
        self.data_port = data_port
        self.aux_port = aux_port
        self.cmd_port = cmd_port

        self.num_emg_channels = 16
        self.num_imu_channels = 16 * 9
        self.frequencies = [1, 5, 7, 8]

        self.running = multiprocessing.Value('b', False)
        self.stop_event = multiprocessing.Event()
        self.lock = multiprocessing.Lock()

        self.cmd_socket = None
        self.data_socket = None
        self.aux_socket = None

    @staticmethod
    def modify_data(data):
        data[::2] *= 2
        return data

    def handle_commands(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.cmd_socket:
            self.cmd_socket.bind((self.host, self.cmd_port))
            self.cmd_socket.listen(1)
            print("Oczekiwanie na połączenie z klientem (komendy)...")
            conn_cmd, addr = self.cmd_socket.accept()
            print(f"Połączono z klientem {addr} (komendy)")

            while not self.stop_event.is_set():
                try:
                    conn_cmd.sendall(b"1")
                    cmd_data = conn_cmd.recv(1024).decode().strip()
                    if cmd_data == "START":
                        print("Odebrano START")
                        with self.lock:
                            self.running.value = True
                        conn_cmd.sendall(b"OK")
                    elif cmd_data == "STOP":
                        print("Odebrano STOP")
                        with self.lock:
                            self.running.value = False
                        break
                except socket.timeout:
                    continue

            conn_cmd.close()

    def send_emg_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.data_socket:
            self.data_socket.bind((self.host, self.data_port))
            self.data_socket.listen(1)
            print("Oczekiwanie na połączenie dla danych EMG...")
            conn_data, _ = self.data_socket.accept()
            print("Połączono z klientem dla danych EMG")

            t = 0
            while not self.running.value:
                time.sleep(0.1)

            while self.running.value:
                emg_data = np.array([
                    np.sin(2 * np.pi * self.frequencies[i % 4] * t + (i * np.pi / self.num_emg_channels))
                    for i in range(self.num_emg_channels)
                ]).astype(np.float32)
                emg_data = self.modify_data(emg_data)
                packet = struct.pack('<' + 'f' * self.num_emg_channels, *emg_data)
                conn_data.sendall(packet)
                time.sleep(0.01)
                t += 0.01

            conn_data.close()

    def send_imu_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.aux_socket:
            self.aux_socket.bind((self.host, self.aux_port))
            self.aux_socket.listen(1)
            print("Oczekiwanie na połączenie dla danych IMU...")
            conn_aux, _ = self.aux_socket.accept()
            print("Połączono z klientem dla danych IMU")

            while not self.running.value:
                time.sleep(0.1)

            while self.running.value:
                imu_data = np.random.rand(self.num_imu_channels).astype(np.float32)
                imu_data = self.modify_data(imu_data)
                packet = struct.pack('<' + 'f' * self.num_imu_channels, *imu_data)
                conn_aux.sendall(packet)
                time.sleep(0.1)

            conn_aux.close()
            print("Zamknięto połączenie danych IMU")

    def stop_transmission(self):
        self.stop_event.set()
        with self.lock:
            self.running.value = False

        print("Zatrzymywanie transmisji...")

        time.sleep(0.2)

        if self.cmd_socket:
            self.cmd_socket.close()
        if self.data_socket:
            self.data_socket.close()
        if self.aux_socket:
            self.aux_socket.close()

        print("Zatrzymano transmisję i zamknięto gniazda.")

    def run(self):
        cmd_thread = threading.Thread(target=self.handle_commands, daemon=True)
        emg_thread = threading.Thread(target=self.send_emg_data, daemon=True)
        imu_thread = threading.Thread(target=self.send_imu_data, daemon=True)

        cmd_thread.start()
        emg_thread.start()
        imu_thread.start()

        cmd_thread.join()
        emg_thread.join()
        imu_thread.join()

        print("Zakończono działanie wszystkich wątków.")

        # self.terminate()
        # self.join()

if __name__ == "__main__":
    simulator = TrignoDataSimulator()
    simulator.start()
    simulator.join()