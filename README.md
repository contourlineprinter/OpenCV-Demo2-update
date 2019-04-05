# OpenCV-Demo2-update
A better version which can filter the background and give better image quality for final countour line image

Design pattern
1.Reduce the number of points (vertices) in the contours
Each contour can be represented by a set of vertices, connecting these vertices makes the netire contour. Like rectangular contour can be represented by four corner points joing the points.
More complex contour can also represented by same approach. Polygon approximation method is used to reducing the number of vertices which means a few set of points can approximate the overall structure or shape of the contour. Increasing the smoothing parameter will reduce the number of points but it will lead more straight lines and less related to original shape. In contrast, low error margin will retain the original shape but have more points.

2. Fileter complex background from the image
For this case, we are trying to filter those contour with lower area amount, and assumpt that the largest area is representing the main object of the image. So after detect edges, we find contours and create a mast to pick the contour having the largest area and draw it to it. Then fill the mask to and smooth the mast using dilate and erode operation. Then blur the mask to remove any gap. In the last step, we apply the mask on original image and leave other background erased. Final image will be image contain in the mask.
Issue: Main issue is that there are many patterns of background. The assumption is to mask the largest area of contour. However, not every image will hold this pattern. Some picture may have multiple main objects, or the background is larger than main object and so on. Deeper research will be needed if we want to deal with more kinds of image, and it can be accomplished in demo 3.
