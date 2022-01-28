import imutils
import cv2
import os
import numpy as np

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def neuralStyleTransfer(directoryName, filename, selected_style):

	target = os.path.join(APP_ROOT, 'static/models/')
	net = cv2.dnn.readNetFromTorch(target + selected_style)

	image = cv2.imread(directoryName+filename)
	image = imutils.resize(image, width=600)
	(h, w) = image.shape[:2]

	blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
		(103.939, 116.779, 123.680), swapRB=False, crop=False)
	net.setInput(blob)

	output = net.forward()

	output = output.reshape((3, output.shape[2], output.shape[3]))
	output[0] += 103.939
	output[1] += 116.779
	output[2] += 123.680
	output = output.transpose(1, 2, 0)

	filename, file_extension = os.path.splitext(filename)
	print(filename)
	newFileName = 'processedImg'+ '_' + filename + file_extension
	cv2.imwrite(directoryName + newFileName, output)
	print(newFileName)
	print(directoryName)

	return newFileName

if __name__=='__main__':
    neuralStyleTransfer('/Users/sandarali.usindh/Documents/pyFlaskCV/images', 'bbq.jpg', 'gold_black_2700.t7')