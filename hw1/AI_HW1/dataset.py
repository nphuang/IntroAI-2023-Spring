import os
import cv2

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    """
    subdir should be one of face or non-face, because dataPath is train or test. 
    If it is a face, set the label to 1, otherwise 0. 
    And traverse each image file in the subdir, use the imread() function to read
    image in grayscale, and append array of image and label into dataset.
    """
    dataset = []

    for subdir in os.listdir(dataPath):  # loop through train/test directories
        subdirPath = os.path.join(dataPath, subdir)
        if os.path.isdir(subdirPath):
            label = 1 if subdir == 'face' else 0
            for filepath in os.listdir(subdirPath):  # loop through image files
                imgPath = os.path.join(subdirPath, filepath)
                imgArr = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
                dataset.append((imgArr, label))
    # End your code (Part 1)
    return dataset
