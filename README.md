# OpenCV-Demo2-update
A better version which can filter the background and give better image quality for final countour line image

Design pattern
1.Reduce the number of points (vertices) in the contours
Each contour can be represented by a set of vertices, connecting these vertices makes the netire contour. Like rectangular contour can be represented by four corner points joing the points.
More complex contour can also represented by same approach. Polygon approximation method is used to reducing the number of vertices which means a few set of points can approximate the overall structure or shape of the contour. Increasing the smoothing parameter will reduce the number of points but it will lead more straight lines and less related to original shape. In contrast, low error margin will retain the original shape but have more points.

2. Fileter complex background from the image
For this case, we are trying to filter those contour with lower area amount, and assumpt that the largest area is representing the main object of the image. So after detect edges, we find contours and create a mast to pick the contour having the largest area and draw it to it. Then fill the mask to and smooth the mast using dilate and erode operation. Then blur the mask to remove any gap. In the last step, we apply the mask on original image and leave other background erased. Final image will be image contain in the mask.
Issue: Main issue is that there are many patterns of background. The assumption is to mask the largest area of contour. However, not every image will hold this pattern. Some picture may have multiple main objects, or the background is larger than main object and so on. Deeper research will be needed if we want to deal with more kinds of image, and it can be accomplished in demo 3.


There are possible approach or algorithms which we can use alone or in combination of each other for improvement of background filter.
1.Interactive foreground extraction using grab-cut algorithm.
2.Extracting foreground using watershed transformations.
3.Gaussian Mixture-based Background/Foreground Segmentation Algorithm.
4.Background Subtraction Based on colour and Depth approach.
5.Background removal using robust PCA.

This is a big design pattern, the testing scripts is still implementing. 

OpenCV-Demo3-backgroundfilter design
grab=cut is useful approach for selecting the main object and removing evertying outside the object as background. It also removes any pattern similar to background within the main object. The compare area method in last demo is also combined in this approach.
1.Fixing the rectangle for the main object
2.Apply grab-cout on the image using the rectangel defined above
3. Apply mask on the original image leaving background details
4. pass the converted image to next step as input image
5. convert image to grayscale
6. detect edges and find contours
7. create a mask, so pick the contour having the largest area dn draw it on the mask
8.fill the mask to close the optn path
9.smooth the mak using dilate and erode operation
10.blur the mask to remove any gap in the path
11.apply the mak on the original image, this will leave other background and leave main object inside the mask
12.final image will have image contained within the mask boudary

issues: image is still rough and may mask wrong object if the setting is not correct. Also, if there are multiple main objects, I still do not have a efficient way to mask the background and leave multiple background. 
