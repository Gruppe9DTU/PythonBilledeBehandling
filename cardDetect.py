import cv2

#Init lists of classifiers
typelist = []
typelist.append([cv2.CascadeClassifier('Cascade/h.xml'), 1])
typelist.append([cv2.CascadeClassifier('Cascade/s.xml'), 2])
typelist.append([cv2.CascadeClassifier('Cascade/r.xml'), 3])
typelist.append([cv2.CascadeClassifier('Cascade/k.xml'), 4])

#Find type of card
def findtype(img):
    r=0
    cur=0   #Increase for higher requirements for detection
    x = img.shape
    if img is None: return 0
    
    #----------Suit enhancer----------
    thresh, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    img = cv2.resize(img,(int(x[1]*2),int(x[0]*2)))
    
    for (cas,i) in typelist:
        c=cas.detectMultiScale(img,1.001,0)
        if len(c)>cur:                    #If this type has the most detections, r is of this type
            cur=len(c)
            r=i
        '''elif len(c)==cur and len(c)!=0:   #If this type has the the same amount of detections as the current type, r is debatable
            r=5 #TODO Only needed if we add support as it will almost never happen'''
    return r

#Splits the image to lessen memory load on detectMultiScale
def imagesplit(img, row=1, col=1):
    results=[]
    s = img.shape
    y = s[0]//row
    x = s[1]//col
    for i in range(row):
        for j in range(col):
            results.append([img[i*y:i*y+y,j*x:j*x+x],j*x,i*y])
    return results


#Find card and value
def find(img, row=1, col=1):
    result=[]
    split = imagesplit(img, row, col)
    for i in range(14):
        cas = cv2.CascadeClassifier('Cascade/'+str(i)+'.xml')
        if cas.empty(): continue
        for (temp,j,k) in split:
            c=cas.detectMultiScale(temp,1.01,7,0,(15,15),(90,90))
            for (x,y,w,h) in c:
                if i==0:
                    result.append([x+j,y+k,w,h,i,0])
                    continue
                img2 = temp[y+h//2:y+h*3,x-w//4:x+w+w//4]   #Cut a piece of the card
                t=findtype(img2)                            #Find type for the given value
                if t!=0: result.append([x+j,y+k,w,h,i,t])   #No type, no card
    cas = None
    return result


#Test
if __name__ == "__main__":
    img=cv2.imread("3.jpg")
    print(img.shape)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    r=find(img,2,2)
    print(r)
    hid=0
    deb=0
    #thresh, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
    for (x,y,w,h,i,j) in r:
        cv2.rectangle(img,(x,y),(x+w,y+h),(155,0,0),2)
        if j==0: 
            #print("-"+str(i))
            hid=hid+1
        if j==5: deb=deb+1
        print(str(i)+"|"+str(j))
        cv2.imshow("1",img[y+h//2:y+h*3,x-w//4:x+w+w//4])
        cv2.waitKey()#'''
    print(len(r))
    print(str(hid)+"|"+str(deb))
    '''for im in imagesplit(img, 1, 2):
        cv2.imshow("1",im[0])
        cv2.waitKey()
    #'''
