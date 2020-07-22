import cv2
import numpy as np

img = cv2.imread('./Anh/Phong-tri-benh-vang-la-Greening-tren-cay-co-mui.jpg')
original = img.copy()
cv2.imshow('original',original)
blur = cv2.GaussianBlur(img,(11,11),1)
canny = cv2.Canny(blur, 100, 290)
canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
cv2.imshow('original',canny)

bordered = cv2.cvtColor(canny,cv2.COLOR_BGR2GRAY)
contours,hierarchy = cv2.findContours(bordered, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

maxC = 0
for x in range(len(contours)):
	if len(contours[x]) > maxC:
		maxC = len(contours[x])
		maxid = x

print('max',contours[maxid])







cv2.waitKey()


