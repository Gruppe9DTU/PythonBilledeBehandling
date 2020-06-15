import time, threading, socket, cv2, numpy as np

HOST = '192.168.0.51'
PORT = 8888

def getImage():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection")
        conn,addr = s.accept()
        newData = bytearray()
        with conn:
            print('Connected by', addr)
            while True:
                sizeOfData = conn.recv(1024)
                #sizeOfData = int.from_bytes(sizeOfData,byteorder='big')
                #print("Indhold: "+sizeOfData)
                while len(newData) < int(sizeOfData):
                    packet = conn.recv(int(sizeOfData) - len(newData))
                    if not packet:
                        continue
                    newData.extend(packet)
                #newData = conn.recv(48000000)
                #mat = np.array(newData)
                #mat=list(newData)
                for x in range(20):
                    print(newData[x])

                
                nparr = np.frombuffer(newData, np.uint8)#.reshape(3000, 4000)
                #print(nparr.size)
                mat = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                imS = cv2.resize(mat, (960, 540))
                
                if not (np.array_equal(mat,None)):
                #if not mat is None and mat != '':
                    cv2.imshow("Test",imS)
                    imageReq(mat)


def imageReq(img):
    global cascade
    c = cascade.detectMultiScale(img)
    
    for (x,y,w,h) in c:
        print("tal")
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.imshow('img',img)
    
    while 1:
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


def initClassifier():
    global cascade
    cascade = cv2.CascadeClassifier('cascade_6.xml')




if __name__ == "__main__":
    initClassifier()
    while(True):
        getImage()