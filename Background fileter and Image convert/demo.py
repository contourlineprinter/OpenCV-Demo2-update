import numpy as np
import cv2
import matplotlib.pyplot as plt
from ImageConversionClass import ImageConversion

#-----------------------------------------         
name = "2.jpg"
path = "./" + name
tmp_name = "tmp.jpg"
formatted_path = "./" + tmp_name

def remove_background(path, formatted_path):
    BLUR = 15 # Blur size
    DILATE = 8
    ERODE = 8
    THRESH1 = 15
    THRESH2 = 180
    COLOR = (1.0, 1.0, 1.0) # Mask color
    # Reading image from the specified path
    img = cv2.imread(path)
    # Using canny, dilate and erode together to detect edges
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, THRESH1, THRESH2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    c_info = []
    # Finding contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        c_info.append((c, cv2.isContourConvex(c), cv2.contourArea(c),))

    # Sorting contours based on area
    c_info = sorted(c_info, key=lambda c: c[2], reverse=True)

    # Idea is to draw an empty mask
    # and drawing a filled polygon of largest contour
    # on it.
    max_contour = c_info[0]
    image_mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(image_mask, max_contour[0], (255))

    # Smoothing the mask
    image_mask = cv2.dilate(image_mask, None, iterations=DILATE)
    image_mask = cv2.erode(image_mask, None, iterations=ERODE)
    # Applying gaussian blur to the mask
    image_mask = cv2.GaussianBlur(image_mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([image_mask] * 3)
    mask_stack = mask_stack.astype('float32') / 255.0
    img = img.astype('float32') / 255.0

    # Blending original image with the maske.
    masked = (mask_stack * img) + ((1 - mask_stack) * COLOR)
    masked = (masked * 255).astype('uint8')
    # Rewriting image back
    cv2.imwrite(formatted_path, masked)

remove_background(path, formatted_path)

# create an ImageConversion object

imgConvert1 = ImageConversion(tmp_name, formatted_path)

# print class documentation
print ("ImageConversion.__doc__:", ImageConversion.__doc__)

# print employee
imgConvert1.printImgInfo()

# load in image
img = imgConvert1.readImageOriginal(tmp_name)
imgGray = imgConvert1.readImageGrayscale(tmp_name)

# show image
imgConvert1.showImage("Original Image", img)

# get image ready
eroImg = imgConvert1.getImageReady(imgGray)

# find contour lines not using Canny edges
conImgNoEdgeOld, conImgNoEdge, conNoEdgePoints = imgConvert1.createContours(eroImg)

# compare three images - original, edges found, final contour image 
imgConvert1.showThreeImages(img, conImgNoEdgeOld, conImgNoEdge, "Original", "Edges Found", "Final Contour")

# close all windows
imgConvert1.closeAllWindows()

#-----------------------------------------
