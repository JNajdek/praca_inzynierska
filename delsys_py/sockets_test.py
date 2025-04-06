import socket
import struct
import numpy as np
import time
import threading

# Definiowanie adresu IP i portów
HOST = 'localhost'  # Lokalny host
DATA_PORT = 50043  # Port dla danych EMG
AUX_PORT = 50044  # Port dla danych IMU
CMD_PORT = 50040  # Port dla komend sterujących (TCP)

# Rozmiary pakietów
NUM_EMG_CHANNELS = 16
NUM_IMU_VALUES = 16 * 9  # 16 zestawów po 9 wartości

# Częstotliwości dla różnych wariantów
FREQUENCIES = [1, 5, 7, 8]

running = False
lock = threading.Lock()

def modify_data(data):
    """Modyfikuje dane: co drugi kanał ma 2x większą amplitudę."""
    data[::2] *= 2  # Zwiększa co drugi element
    return data

def handle_commands():
    """Obsługuje komendy START/STOP."""
    global running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cmd_socket:
        cmd_socket.bind((HOST, CMD_PORT))
        cmd_socket.listen(1)
        print("Oczekiwanie na połączenie z klientem (komendy)...")
        conn_cmd, addr = cmd_socket.accept()
        print(f"Połączono z klientem {addr} (komendy)")

        while True:
            try:
                conn_cmd.sendall(b"1")
                cmd_data = conn_cmd.recv(1024).decode().strip()
                if cmd_data == "START":
                    print("Odebrano START")
                    with lock:
                        running = True
                    conn_cmd.sendall(b"OK")
                elif cmd_data == "STOP":
                    print("Odebrano STOP")
                    with lock:
                        running = False
                    break
            except socket.timeout:
                continue

        conn_cmd.close()

def send_emg_data():
    """Wysyła dane EMG w formacie 16 wartości float32."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as data_socket:
        data_socket.bind((HOST, DATA_PORT))
        data_socket.listen(1)
        print("Oczekiwanie na połączenie dla danych EMG...")
        conn_data, _ = data_socket.accept()
        print("Połączono z klientem dla danych EMG")

        t = 0  # Czas początkowy
        while True:
            with lock:
                if running:
                    break
        pass

        while True:
            with lock:
                if not running:
                    break

            # Generowanie danych EMG z różnymi częstotliwościami
            emg_data = np.array([
                np.sin(2 * np.pi * FREQUENCIES[i % 4] * t + (i * np.pi / NUM_EMG_CHANNELS))
                for i in range(NUM_EMG_CHANNELS)
            ]).astype(np.float32)

            emg_data = modify_data(emg_data)

            # Pakowanie danych w format float32 ('f')
            packet = struct.pack('<' + 'f' * NUM_EMG_CHANNELS, *emg_data)
            conn_data.sendall(packet)
            print("Wysłano dane EMG")

            time.sleep(0.01)
            t += 0.01

        conn_data.close()

def send_imu_data():
    """Wysyła dane IMU w formacie float32."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as aux_socket:
        aux_socket.bind((HOST, AUX_PORT))
        aux_socket.listen(1)
        print("Oczekiwanie na połączenie dla danych IMU...")
        conn_aux, _ = aux_socket.accept()
        print("Połączono z klientem dla danych IMU")

        while True:
            with lock:
                if running:
                    break
        pass

        while True:
            with lock:
                if not running:
                    break

            # Generowanie losowych danych IMU
            imu_data = np.random.rand(NUM_IMU_VALUES).astype(np.float32)
            imu_data = modify_data(imu_data)

            # Pakowanie danych w format float32 ('f')
            packet = struct.pack('<' + 'f' * NUM_IMU_VALUES, *imu_data)
            conn_aux.sendall(packet)
            print("Wysłano dane IMU")

            time.sleep(0.1)

        conn_aux.close()
        print("Zamknięto połączenie danych IMU")

# Tworzenie i uruchamianie wątków
cmd_thread = threading.Thread(target=handle_commands, daemon=True)
emg_thread = threading.Thread(target=send_emg_data, daemon=True)
imu_thread = threading.Thread(target=send_imu_data, daemon=True)

cmd_thread.start()
emg_thread.start()
imu_thread.start()

cmd_thread.join()
emg_thread.join()
imu_thread.join()

print("Zakończono działanie wszystkich wątków.")