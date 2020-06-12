import os, time, threading, socket, cv2

HOST = '192.168.0.51'
PORT = 8888

def getImage():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for connection")
        conn,addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                newData = conn.recv(1024).decode()
                if not newData is None and newData != '':
                    imageReq(newData)



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
    
    