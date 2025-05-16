import cv2

# homography routine


def calculate_centroid(cap):
    _, frame = cap.read()
    
    # colour settings
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 75, 150)

    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    
    for c in cnts: 
        approx = cv2.approxPolyDP(c, 0.02*cv2.arcLength(c,True), True)
        if len(approx==4) and cv2.isContourConvex(approx) \
            and cv2.contourArea(approx) > 2000:
            M = cv2.moments(approx)
            cx, cy = M['m10']/M['m00'], M['m01']/M['m00']
            # cv2.drawContours(frame,[approx],-1,(0,255,0),2)
            pxl_coords = (int(cx),int(cy))
            # cv2.circle(frame, pxl_coords,4,(0,0,255),-1)
    
    return pxl_coords
    


    

