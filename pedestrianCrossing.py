import cv2
import numpy as np
from skimage.feature import local_binary_pattern
import operator

possiblePedestrianCrossingContour = []
yCentroid = []
crossingCountour =[]
addH = 40
subY = 100
FILE = "/tmp/numberPlateInfo.npy"

class Contour :

	def __init__(self):
	
		self.yCentroid = None
		self.contours = None
		self.fltArea = 0.0
		self.RectX = 0
		self.RectY = 0
		self.RectWidth = 0
		self.RectHeight = 0
		self.id = False

	def everythingAboutContour(self , contours):
		
		[RectX, RectY, RectWidth, RectHeight] = cv2.boundingRect(contours)
		self.contours = contours
		self.RectX = RectX
		self.RectY = RectY
		self.RectWidth = RectWidth
		self.RectHeight = RectHeight
		self.fltArea = cv2.contourArea (self.contours)
		self.aspectRatio = float (self.RectWidth) / self.RectHeight

	def getid(self):
		self.id = True


def readFromFile(img,resizingParameter,zz):

	readInfo = np.load(FILE )

	numberPlateCoordinates = readInfo[:len(readInfo) - 1]
	resizingParameterNP = readInfo[len(readInfo)-1]
	# print numberPlateCoordinates
	# isCrossingPedestrian(numberPlateCoordinates,resizingParameter)
	trueFalse = isCrossingPedestrian(img,numberPlateCoordinates,resizingParameterNP,resizingParameter,zz)
	for i in range(len(trueFalse)):
		if(trueFalse[i]):
			print "vehicle "+str(i+1)+" from left is defaulter"
		else:
			print "vehicle "+str(i+1)+" from left is not a defaulter"

def isCrossingPedestrian(img,numberPlateCoordinates,resizingParameterNP,resizingParameter,zz):
	# print 1
	trueFalse = []

	# print len(numberPlateCoordinates)
	for i in range(len(numberPlateCoordinates)):
		# rectNP = cv2.rectangle(img, (int(numberPlateCoordinates[i][0]/resizingParameter), int(numberPlateCoordinates[i][1]/resizingParameter)-subY), (int((numberPlateCoordinates[i][0] + numberPlateCoordinates[i][3])/resizingParameter), int((numberPlateCoordinates[i][1] + numberPlateCoordinates[i][2] )/resizingParameter)+addH),( 0, 255, 0 ),2 )
		# rectNP = cv2.rectangle(img, (0,0), (imgShape[1], imgShape[0]), (255,0,255), 2)
		# print cv2.clipLine(rectNP, (0,int(zz[1])), (img.shape[1], int(zz[0]*img.shape[1] + zz[1])))
		# return cv2.clipLine(rectNP, (4,5), (8000,9000))[0]
		trueFalse.append(cv2.clipLine((int(numberPlateCoordinates[i][0]/resizingParameter) - subY,int(numberPlateCoordinates[i][1]/resizingParameter), int((numberPlateCoordinates[i][3])/resizingParameter), int((numberPlateCoordinates[i][2])/resizingParameter) + addH), (0,int(zz[1])), (img.shape[1], int(zz[0]*img.shape[1] + zz[1])))[0])
	return trueFalse

img = cv2.imread ("FINL/4.jpg")
imgShape = img.shape [:2]
resizingParameter = imgShape[1] / 1000.0 if (imgShape[1] > imgShape[0]) else imgShape[0] / 1000.0
imgResized = cv2.resize(img, ( int(imgShape[1] / resizingParameter), int(imgShape[0] / resizingParameter)))
imgResizedCopy = imgResized.copy()
imgGray = cv2.cvtColor (imgResized, cv2.COLOR_BGR2GRAY)
imgBlurr = cv2.medianBlur (imgGray, 1, 0)
imgMorph = cv2.morphologyEx (imgBlurr, cv2.MORPH_OPEN, (5,5))
# print imgMorph, imgMorph.shape
radius = 30
no_points = 8
lbp = local_binary_pattern(imgMorph, no_points, radius, method = 'uniform')
# cv2.imshow("lbp", lbp)
# cv2.waitKey(0)
lbp = lbp.astype(np.uint8)
thresh, lbpThresh = cv2.threshold (lbp, 1, 255, cv2.THRESH_BINARY_INV)
# print lbpThresh.shape
# cv2.imshow("fuckfuck", lbpThresh)
cv2.waitKey(0)
contours, hierarchy = cv2.findContours (lbpThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in xrange(len(contours)-1):

	contourObj = Contour();
	contourObj.everythingAboutContour(contours[i])

	# [RectX, RectY, RectWidth, RectHeight] = cv2.boundingRect(contours[i])
	# aspectRatio = float(RectWidth) / RectHeight

	if (contourObj.fltArea > 500 and contourObj.fltArea < 7500 and  contourObj.aspectRatio > 3.7 and contourObj.aspectRatio < 50.5):

		M = cv2.moments (contours[i])                  # moments

		contourObj.yCentroid = contourObj.RectY + int (M['m01'] / M['m10'])		
		possiblePedestrianCrossingContour.append (contourObj)
		yCentroid.append (contourObj.yCentroid)

		# print cv2.contourArea(contours[i]) , contourObj.aspectRatio, contourObj.yCentroid

		# cv2.rectangle(imgResized, (contourObj.RectX, contourObj.RectY), (contourObj.RectX + contourObj.RectWidth , contourObj.RectY + contourObj.RectHeight), (255,255,0), 2)

# cv2.imshow ("Contours Found After LBP", imgResized)
# cv2.waitKey(0)

maxCentroid, minCentroid = max(yCentroid), min(yCentroid)

# for x in xrange (imgShape[1], 20):
crossingCount = 0

for y in xrange (minCentroid, maxCentroid, 10):

	match = 0;
	possibleCrossingContours = []

	for centroid in possiblePedestrianCrossingContour :


		if ( y - 25 <= centroid.yCentroid <= y + 25):

			match += 1
			possibleCrossingContours.append(centroid)

	if match > crossingCount:

			crossingCount = match
			crossingCountour = possibleCrossingContours


# print crossingCount, len (crossingCountour)

crossingCountour.sort (key = operator.attrgetter ("RectY"))

xx = []
yy = []

for contour in crossingCountour:

	contour.getid()
	# cv2.rectangle(imgResizedCopy, (contour.RectX, contour.RectY),(contour.RectX + contour.RectWidth, contour.RectY + contour.RectHeight) , (255, 0,0), 2)
	xx.append(contour.RectX)
	yy.append(contour.RectY)


# cv2.rectangle(imgResizedCopy, (crossingCountour[0].RectX, crossingCountour[0].RectY), (crossingCountour[-1].RectX + crossingCountour[-1].RectWidth, crossingCountour[-1].RectY + crossingCountour[-1].RectHeight), (0,255,0), 2)

zz = np.polyfit(xx,yy,1)
# cv2.line (imgResizedCopy, (0,crossingCountour[0].RectY), (imgShape[1], crossingCountour[0].RectY), (0,0,255), 2)
cv2.line (imgResizedCopy, (0,int( zz[1])), (imgResizedCopy.shape[1], int(zz[0]*imgResizedCopy.shape[1] + zz[1])), (0,0,255), 2)
# print int(zz[0] + zz[1]), (imgShape[1], int(zz[0]*imgShape[1] + zz[1]))
# print igmResizedCopy.shape
readFromFile(imgResizedCopy,resizingParameter,zz)
cv2.imshow("Crossings Detected", imgResizedCopy)
cv2.waitKey(0)












		