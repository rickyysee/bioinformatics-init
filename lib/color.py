#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--image', help="Image to open, if desired.")
parser.add_argument('-a', '--min', help='Minimum value to use for color gradient. [X,Y,Z]')
parser.add_argument('-b', '--max', help='Maximum value to use for color gradient. [X,Y,Z]')
parser.add_argument('-f', '--format', help='Type of color model being used by min and max. [HSV (default) or RGB]')

args = parser.parse_args()

print(f'\
Image:  {args.image}\n\
Min:  {args.min}\n\
Max:  {args.max}\n\
Format:  {args.format}\n\
'
)

if args.format is None:
	format = 'HSV' # default format will be HSV
else:
	format = args.format 


def hsv_gradient(min, max, steps):
	hsv_min = np.fromstring(min, sep=',', dtype=np.uint8)
	hsv_max = np.fromstring(max, sep=',', dtype=np.uint8)

	gradient = []
	print(f'Min vector: {hsv_min}')
	print(f'Max vector: {hsv_max}\n')
	for i in range(steps):
		ratio = i / (steps - 1)
		h = hsv_min[0] + (hsv_max[0] - hsv_min[0]) * ratio
		s = hsv_min[1] + (hsv_max[1] - hsv_min[1]) * ratio
		v = hsv_min[2] + (hsv_max[2] - hsv_min[2]) * ratio

		step = (int(h), int(s), int(v))
		gradient.append(step)

	return gradient
	"""
	hsv = np.full((300, 300, 3), hsv_min, dtype=np.uint8)
	hsv_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

	cv2.imshow('HSV Color', hsv_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	"""

def gradient_image(g):
	return

if format == 'HSV':
	g = hsv_gradient(args.min, args.max, 10)
	print(f'\
Gradient vector: \n\
{g}\
	'
	)
	gradient_image(g)

if format == 'RGB':
	print(f'Format is {args.format}')

if args.image is not None:
	img = mpimg.imread(args.image)
	plt.imshow(img)
	plt.show()

