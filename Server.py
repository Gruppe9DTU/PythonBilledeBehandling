import socket, cv2, numpy as np
import cardDetect as cd

HOST = '192.168.0.51'
PORT = 8888

def getImage(conn):
    newData = bytearray()
    print("Waiting for data...")
    sizeOfData = conn.recv(1024)
    if sizeOfData:
        while len(newData) < int(sizeOfData):
            packet = conn.recv(int(sizeOfData) - len(newData))
            if not packet:
                continue
            newData.extend(packet)
        
        nparr = np.frombuffer(newData, np.uint8)
        
        mat = cv2.imdecode(nparr, cv2.IMREAD_REDUCED_GRAYSCALE_8)
        
        if not (np.array_equal(mat,None)):
            result = cd.find(mat)
            
            if result != []:
                test = str(np.concatenate(result, axis=None))+"\n"
                conn.send(test.encode('utf-8'))
                print(test)
            else:
                print("Nothing found")
                conn.send("[]\n".encode('utf-8'))

    else:
        print("Connection lost")
        exit()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection")
        conn,addr = s.accept()
        with conn:
            print('Connected by', addr)
            while(True):
                getImage(conn)
