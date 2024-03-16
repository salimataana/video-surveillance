import socket
import cv2
import pickle
import struct

HOST = ''
NUMERO_PORT = 8485

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket crée avec succès')
s.bind((HOST, NUMERO_PORT))
print('')
s.listen(10)
print(f"Le socket est entrain d'ecouter sur le port : {NUMERO_PORT}")

conn, addr = s.accept()
data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
        if not data:
            cv2.destroyAllWindows()
            conn, addr = s.accept()
            continue
    # reception de la donnée brute des cameras depuis les sockets
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    # dezipper la donnée
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    cv2.imshow('Plateforme', frame)
    cv2.waitKey(1)
