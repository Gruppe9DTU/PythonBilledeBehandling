import socket, cv2, numpy as np
import cardDetect as cd

HOST = '192.168.0.51'
PORT = 8888

def getImage(conn):
    newData = bytearray()
    print("Waiting for data...")
    sizeOfData = conn.recv(1024) # Recieve a message containing the number of incoming bytes.
    if sizeOfData:
        while len(newData) < int(sizeOfData): # As long as we haven't recieved all of our data keep the loop running.
            packet = conn.recv(int(sizeOfData) - len(newData))
            if not packet:
                continue
            newData.extend(packet)
        
        nparr = np.frombuffer(newData, np.uint8) # Get array from string.
        
        mat = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE) # Decode array to matrix (image).
        
        if not (np.array_equal(mat,None)):
            result = cd.find(mat,1,2) # Detect the cards
            
            if result != []:
                print(str(result))
                test = str(np.concatenate(result, axis=None))+"\n" # Make (maybe) multi-dimensional array to an one-dimensional array.
                conn.send(test.encode('utf-8'))
            else:
                print("Nothing found")
                conn.send("[]\n".encode('utf-8')) # Send a message to the client containing an empty array.
        
        return True # The data transfer succeded and the connection is still alive.

    else:
        conn.close()

        print("Connection lost. Waiting for new connection.")

        return False # Lost connection to client
        

if __name__ == "__main__":
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen() # Listen for connections
        print("Waiting for connection")
        while True:
            try:
                conn,addr = s.accept() # Accept connection
                connectionActive = True
                
                with conn:
                    print('Connected by', addr)
                    while connectionActive:
                        connectionActive = getImage(conn) # Process the data from the client and change connectionActive depending on connection with client.

            except KeyboardInterrupt:
                s.close() # When user terminates the program remember to free the port.
                exit()
            
            except OSError:
                conn.close() # If client disconnects clean up.