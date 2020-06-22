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
    x = img.shape
    if x[1]>150: x=1.01
    else: x=1.001
    #img = cv2.resize(img,(int(y*2),int(x*2)))
    for (cas,i) in typelist:
        c=cas.detectMultiScale(img,x)
        if r==0 and len(c)!=0: r=i                       #If no former result and detection, r is of this type
        elif r!=0 and len(c)!=0: print("Debatable suit") #If former result and current detection, r is of debatable type
    return r


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
    for i in range(1,14):
        cas = cv2.CascadeClassifier('Cascade/'+str(i)+'.xml')
        if cas.empty(): continue
        for (temp,j,k) in split:
            c=cas.detectMultiScale(temp,1.01,8)
            for (x,y,w,h) in c:
                img2 = temp[y:y+h*3,x:x+w]          #Cut a piece of the card
                t=findtype(img2)                    #Find type for the given value
                result.append([x+j,y+k,w,h,i,t])    #If type, then we have a card
    cas = None
    return result


#Test
if __name__ == "__main__":
    img=cv2.imread("1.jpg")
    print(img.shape)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    r=find(img,2,2)
    print(r)
    print(len(r))
    error=0
    for (x,y,w,h,i,j) in r:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    '''    if j==0: error=error+1
        print(str(i)+"|"+str(j))
        cv2.imshow("1",img[y:y+h*3,x:x+w])
        cv2.waitKey()#'''
    print(error)
    for im in imagesplit(img, 7, 4):
        cv2.imshow("1",im[0])
        cv2.waitKey()
    #'''
