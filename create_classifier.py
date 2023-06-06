import numpy as np
from PIL import Image
import os, cv2


path=os.path.join(os.getcwd()+"/data/dataSet")

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        faceImg=Image.open(imagePath).convert('L');
        faceNp=np.array(faceImg,'uint8')
        #split to get ID of the image
        ID=int(os.path.split(imagePath)[-1].split('.')[1])
        faces.append(faceNp)
        IDs.append(ID)
    return IDs, faces

# Method to train custom classifier to recognize face
def train_classifer():
    # Read all the images in custom data-set
    Ids,faces=getImagesAndLabels(path)

    #Train and save classifier
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces,np.array(Ids))
    recognizer.save('data/classifiers/trainningData.yml')
    cv2.destroyAllWindows()

