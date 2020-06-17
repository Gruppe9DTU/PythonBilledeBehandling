import cv2

#Init lists of classifiers
numlist = []
typelist = []
for i in range(1,14):
    cas = cv2.CascadeClassifier(str(i)+'.xml')
    if not cas.empty(): numlist.append([cas, i])


typelist.append([cv2.CascadeClassifier('h.xml'), 1])
#typelist.append([cv2.CascadeClassifier('k.xml'), 2])
#typelist.append([cv2.CascadeClassifier('s.xml'), 3])
#typelist.append([cv2.CascadeClassifier('r.xml'), 4])
numlist.append([cv2.CascadeClassifier('cascade_6.xml'),6])


#Find type of card
def findtype(img):
    r=0
    for (cas,i) in typelist:
        c=cas.detectMultiScale(img,1.01)
        if r==0 and len(c)!=0: r=i              #If no former result and detection, r is of this type
        elif r!=0 and len(c)!=0: print("ERROR") #If former result and current detection, r is of debatable type
    return r


#Find card and value
def find(img):
    result=[]
    for (cas,i) in numlist:
        c=cas.detectMultiScale(img,1.01)
        for (x,y,w,h) in c:
            img2 = img[y+h:y+h*3,x:x+w]             #Cut a piece of the card
            t=findtype(img2)
            print(t)                        #Find type for the given value
            if t!=0: result.append([x,y,w,h,i,t])   #If type, then we have a card
    return result


#Test
'''
if __name__ == "__main__":
    img=cv2.imread("1.jpg")
    x,y,z = img.shape
    z = y/500
    img = cv2.resize(img,(int(y/z),int(x/z)))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    r=find(gray)
    print(r)
    print(len(r))
    #'''
