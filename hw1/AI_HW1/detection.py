import os
import cv2
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    # Begin your code (Part 4)
    """
    use 'with' to read datapath that is txt file, imageName is file name and peopleNum is number of squares,
    then get very squares' coordinates of upper left and side length and append to people,
    image is read with original, and imageL is read with grayscale.
    for each square, use cv2.resize() to resize the image to 19 x 19,
    use clf.classify() to detect whether square contains a face or not.
    then use cv2.rectangle() to draw red or green square on the image.
    finally, use imwrite() to save the image.
    """
    with open(dataPath, "r") as detectData: 
        for line in detectData: 
            imageName, peopleNum = map(str.strip, line.split()) 
            people = []
            for _ in range(int(peopleNum)): 
                people.append(tuple(map(int, detectData.readline().split()))) 
            image = cv2.imread("data/detect/" + imageName) 
            imageL = cv2.imread("data/detect/" + imageName, cv2.IMREAD_GRAYSCALE)
            for face in people:
                faceImage = cv2.resize(imageL[face[1]:face[1]+face[3], face[0]:face[0]+face[2]], (19, 19), interpolation=cv2.INTER_LINEAR)
                if clf.classify(faceImage) == 1:
                    cv2.rectangle(image, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (0, 255, 0), thickness=2)
                else:
                    cv2.rectangle(image, (face[0], face[1]), (face[0] + face[2], face[1] + face[3]), (0, 0, 255), thickness=2)
            cv2.imwrite("result//result_"+imageName, image)
    # End your code (Part 4)
