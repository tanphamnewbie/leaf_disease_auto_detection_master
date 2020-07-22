import cv2

img = cv2.imread('./Anh/images (2).jpg')

#img = cv2.resize(img ,((int)(img.shape[1]/3),(int)(img.shape[0]/3)))
original = img.copy()
neworiginal = img.copy()
blur = cv2.GaussianBlur(img,(11,11),1)
canny = cv2.Canny(blur,50, 290)
canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
cv2.imshow('canny', canny)
bordered = cv2.cvtColor(canny,cv2.COLOR_BGR2GRAY)
contours,hierarchy = cv2.findContours(bordered, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
maxC = 0
for x in range(len(contours)):
	if len(contours[x]) > maxC:
		maxC = len(contours[x])
		maxid = x
cv2.drawContours(neworiginal,contours[maxid],-1,(0,0,255))
cv2.imshow('Contour',neworiginal)
cv2.imwrite('Contour complete leaf.jpg',neworiginal)

height, width, _ = canny.shape
min_x, min_y = width, height
max_x = max_y = 0
frame = canny.copy()

for contour, hier in zip(contours, hierarchy):
	(x,y,w,h) = cv2.boundingRect(contours[maxid])
	min_x, max_x = min(x, min_x), max(x+w, max_x)
	min_y, max_y = min(y, min_y), max(y+h, max_y)
	if w > 80 and h > 80:
		cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 0, 0), 2)
		roi = img[y:y+h , x:x+w]
		originalroi = original[y:y+h , x:x+w]
		
if (max_x - min_x > 0 and max_y - min_y > 0):
	roi = img[min_y:max_y , min_x:max_x]	
	originalroi = original[min_y:max_y , min_x:max_x]
	cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 0, 0), 2)
cv2.imshow('ROI', frame)
cv2.imshow('rectangle ROI', roi)
cv2.imwrite('Cropped Img.jpg',roi)

cv2.waitKey()
