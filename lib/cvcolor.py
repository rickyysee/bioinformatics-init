#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

parser = argparse.ArgumentParser()

# add arguments to take various user inputs
parser.add_argument('-i', '--image', help="Image to open, if desired.")
parser.add_argument('-a', '--min', help='Minimum value of color gradient. ["X,Y,Z"]')
parser.add_argument('-b', '--max', help='Maximum value of color gradient. ["X,Y,Z"]')
parser.add_argument('-f', '--format', help='Type of color model being used by min and max. [HSV (default) or RGB]')
parser.add_argument('-n', '--steps', help="Number of steps to use for the gradient.")
parser.add_argument('-o', '--out', help='Optional: create an output file for the gradient image.')

args = parser.parse_args()

# print out arguments for verification
print(f'\
Image:  {args.image}\n\
Min:  {args.min}\n\
Max:  {args.max}\n\
Format:  {args.format}\n\
Steps: {args.steps}\n\
Output: {args.out}\n\
'
)

if args.format is None:
	format = 'HSV' # default format will be HSV
else:
	format = args.format 

if args.steps is None:
	steps = 10 # default steps will be 10
else:
	steps = int(args.steps)

def calc_gradient(min, max, steps):
	# convert min and max values to ints
	col_min = np.fromstring(min, sep=',', dtype=np.uint8)
	col_max = np.fromstring(max, sep=',', dtype=np.uint8)

	# initialize empty vector
	gradient = []
	# print(f'Min vector: {col_min}')
	# print(f'Max vector: {col_max}\n')
	
	# iterate from min to max value using linear interpolation with specified steps
	for i in range(steps):
		ratio = i / (steps - 1)
		a = col_min[0] + (col_max[0] - col_min[0]) * ratio
		b = col_min[1] + (col_max[1] - col_min[1]) * ratio
		c = col_min[2] + (col_max[2] - col_min[2]) * ratio

		# add this iteration to the gradient vector
		step = (int(a), int(b), int(c))
		gradient.append(step)

	return gradient

def draw_gradient(gradient, hsv, width=512, height=100):
	# define amount of drawing steps as length of gradient
	steps = len(gradient)
	# initialize empty image
	image = np.zeros((height, width, 3), dtype=np.uint8)

	# for each item in gradient vector, compose image
	for i, (a, b, c) in enumerate(gradient):
		# calculate x range for this item
		x_start = int(i * width / steps)
		x_end = int((i + 1) * width / steps)

		# fill x_start to x_end column with this item (color)
		if hsv == 1:
			image[:, x_start:x_end] = [a, b, c]
		else: 
			image[:, x_start:x_end] = [c, b, a] # OpenCV uses BGR, so flip values if using RGB format

	if hsv == 1:
		image_bgr = cv2.cvtColor(image, cv2.COLOR_HSV2BGR) # convert HSV to BGR
		return image_bgr
	else:
		return image

if args.min and args.max is not None: # ensure gradient is only calculated if min and max are given
	if format == 'HSV':
		gradient = calc_gradient(args.min, args.max, steps)
		image_gradient = draw_gradient(gradient, hsv=1)

	if format == 'RGB':
		gradient = calc_gradient(args.min, args.max, steps)
		image_gradient = draw_gradient(gradient, hsv=0)

	# if output is specified, save image
	if args.out is not None:
		file = args.out
		cv2.imwrite(file, image_gradient)

	# print the values of the calculated gradient
	print(f'\
Gradient vector: \n\
{gradient}\
'
	)

	# use cv2 to open a window with the calculated gradient
	cv2.imshow("Gradient", image_gradient)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

# open a specified image
if args.image is not None:
	img = mpimg.imread(args.image)
	plt.imshow(img)
	plt.show()