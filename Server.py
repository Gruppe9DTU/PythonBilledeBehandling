import socket, cv2, numpy as np
import cardDetect as cd

HOST = '192.168.0.51'
PORT = 8889

def getImage(conn):
    newData = bytearray()
    print("Waiting for data...")
    sizeOfData = None
    sizeOfData = conn.recv(1024)
    if sizeOfData:
        while len(newData) < int(sizeOfData):
            packet = conn.recv(int(sizeOfData) - len(newData))
            if not packet:
                continue
            newData.extend(packet)
            
        nparr = np.frombuffer(newData, np.uint8)

        mat = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        imS = cv2.resize(mat, (960, 540))
        
        if not (np.array_equal(mat,None)):
            result = cd.find(mat)
            
            if result != []:
                test = str(np.concatenate(result, axis=None))+"\n"
                conn.send(test.encode('utf-8'))
                print(test)
            else:
                conn.send("[]\n".encode('utf-8'))
            
    else:
        print("Connection lost")
        exit()


def imageReq(img):
    global cascade
    c = cascade.detectMultiScale(img,1.01)
    for (x,y,w,h) in c:
        print("tal")
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        result = cv2.resize(img, (960, 540))
        cv2.imshow('img',result)
    
    while 1:
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    
    return np.concatenate(c, axis=None)


def initClassifier():
    global cascade
    cascade = cv2.CascadeClassifier('cascade_6.xml')


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
