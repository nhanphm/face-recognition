import cv2
from time import sleep
from PIL import Image
from datetime import datetime
from database import getProfile, insertOrUpdateAttendance 

def main_app():
        
        face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(f"./data/classifiers/trainningData.yml")
        cap = cv2.VideoCapture(0)
        pred = 0
        while True:
            ret, frame = cap.read()
            #default_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,1.3,5)

            for (x,y,w,h) in faces:


                roi_gray = gray[y:y+h,x:x+w]

                id,confidence = recognizer.predict(roi_gray)
                profile=getProfile(id)
                #confidence = 100 - int(confidence)
                if profile != None and confidence >=30 and confidence <=80:
                            label = str(profile[1]).upper() + ' - Conf: ' + str(int(confidence))
                    #if u want to print confidence level
                            #confidence = 100 - int(confidence)
                            pred += +1
                            font = cv2.FONT_HERSHEY_PLAIN
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            frame = cv2.putText(frame, label, (x, y-4), font, 1, (0, 255, 0), 1, cv2.LINE_AA)

                else:   
                            pred += -1
                            text = "UnknownFace - conf:" + str(confidence)
                            font = cv2.FONT_HERSHEY_PLAIN
                            frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                            frame = cv2.putText(frame, text, (x, y-4), font, 1, (0, 0,255), 1, cv2.LINE_AA)

            cv2.imshow("image", frame)


            if cv2.waitKey(20):
                print(pred)
                if pred > 20 : 
                    dim =(124,124)
                    img = cv2.imread(f"./data/dataSet/User.{id}.{pred}.jpg", cv2.IMREAD_UNCHANGED)
                    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
                    cv2.imwrite(f"./data/dataSet/User.{id}.50.jpg", resized)
                    Image1 = Image.open(f"./2.png") 
                    
                    # add event to database
                    now = datetime.now()
                    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                    insertOrUpdateAttendance(id, dt_string)
                    # make a copy the image so that the  
                    # original image does not get affected 
                    Image1copy = Image1.copy() 
                    Image2 = Image.open(f"./data/dataSet/User.{id}.50.jpg") 
                    Image2copy = Image2.copy() 
                      
                    # paste image giving dimensions 
                    Image1copy.paste(Image2copy, (195, 114)) 
                      
                    # save the image  
                    Image1copy.save("end.png") 
                    frame = cv2.imread("end.png", 1)

                    cv2.imshow("Attendence",frame)
                    cv2.waitKey(10000)
                    cv2.destroyWindow('Attendence')
                    pred = 0

            if cv2.waitKey(20) & 0xFF == ord('q'):
                break                   

        cap.release()
        cv2.destroyAllWindows()
        
