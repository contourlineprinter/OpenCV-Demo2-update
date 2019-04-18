import cv2
import numpy as np
from matplotlib import pyplot as plt

BLUR = 15
DILATE = 8
ERODE = 8
THRESH1 = 15
THRESH2 = 180
COLOR = (1.0, 1.0, 1.0)

type = 2

img_file = 'bg2.jpg'
x1 = 0.0
x2 = 1.0
y1 = 0.4
y2 = 1.0

img = cv2.imread(img_file)
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
height, width = image_rgb.shape[:2]
rectangle = (int(width*x1), int(height*y1), int(width*x2), int(height*y2))

mask = np.zeros(image_rgb.shape[:2], np.uint8)
bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

cv2.grabCut(image_rgb, mask, rectangle,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

mask_2 = np.where((mask==2) | (mask==0), 0, 1).astype('uint8')

image_rgb_nobg = image_rgb * mask_2[:, :, np.newaxis]

gray = cv2.cvtColor(image_rgb_nobg, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, THRESH1, THRESH2)
edges = cv2.dilate(edges, None)
edges = cv2.erode(edges, None)

c_info = []
contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

for c in contours:
    c_info.append((c, cv2.isContourConvex(c), cv2.contourArea(c),))

c_info = sorted(c_info, key=lambda c: c[2], reverse=True)
max_contour = c_info[0]
image_mask = np.zeros(edges.shape)
cv2.fillConvexPoly(image_mask, max_contour[0], (255))
image_mask = cv2.dilate(image_mask, None, iterations=DILATE)
image_mask = cv2.erode(image_mask, None, iterations=ERODE)
image_mask = cv2.GaussianBlur(image_mask, (BLUR, BLUR), 0)
mask_stack = np.dstack([image_mask] * 3)
mask_stack = mask_stack.astype('float32') / 255.0
img = img.astype('float32') / 255.0
masked = (mask_stack * img) + ((1 - mask_stack) * COLOR)
masked = (masked * 255).astype('uint8')
cv2.imwrite("output.jpg", masked)
plt.imshow(masked), plt.axis("off")
plt.show()
