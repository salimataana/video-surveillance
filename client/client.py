import pickle
import socket
import struct

import cv2
import imutils

# Si le client et le serveur sont sur la meme machine, IP sera : 127.0.0.1
SERVER_IP = '127.0.0.1'
NUMERO_PORT = 8485

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, NUMERO_PORT))
print(f"Connection etablie avec le serveur sur le port {NUMERO_PORT}")
# lire mon webcam
cam = cv2.VideoCapture(0)
img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()

    frame = imutils.resize(frame, width=320)

    frame = cv2.flip(frame, 180)
    result, image = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(image, 0)
    size = len(data)

    if img_counter % 10 == 0:
        client_socket.sendall(struct.pack(">L", size) + data)
        print(f"Envoi de données {img_counter / 10}")

    img_counter += 1

cam.release()
