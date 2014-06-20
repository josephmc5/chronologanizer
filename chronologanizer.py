#!/usr/bin/env python
"""
Chronologanizer is a simple script to organizer your pictures based on
the year, month, date, and time it was taken.

Joe McWilliams <github@joemcwilliams.com>
"""

import exifread
import argparse
import os
import re
import sys
import shutil
from datetime import datetime

def getImageDate(path_name):
	"""Returns a date object of the time the picture given was taken."""

	f = open(path_name, 'rb')
	tags = exifread.process_file(f, stop_tag='Image DateTime')
	if 'Image DateTime' in tags:
		# expects format like 2013:11:24 18:38:01
		return datetime.strptime(str(tags['Image DateTime']),'%Y:%m:%d %H:%M:%S')

def copyToDir(file, destination_dir):
	"""
	Copies the given file into the destination directory with the date structure

	destination directory/year/month/day/time of photo.jpg
	"""

	if (not re.match('.jp[e]?g', os.path.splitext(file)[1], flags=re.IGNORECASE)):
		return

	date = getImageDate(file)

	if not date:
		return

	full_destination_path = os.path.join(destination_dir, date.strftime('%Y'), date.strftime('%m'), date.strftime('%d'))

	if not os.path.exists(full_destination_path):
		print "Creating " + full_destination_path
		os.makedirs(full_destination_path)

	shutil.copy2(file, os.path.join(full_destination_path, date.strftime('%I_%M_%S_%p.jpg')))
	return True

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--input', default='.')
	parser.add_argument('-o', '--output', default='/tmp/')
	args = parser.parse_args()

	input_dir = os.path.normpath(os.path.expanduser(args.input))
	output_dir = os.path.normpath(os.path.expanduser(args.output))

	if (not os.path.exists(input_dir)):
		print "Input path does not exist: " + input_dir
		sys.exit(1)


	print "Looking for pictures in " + input_dir

	for root, subFolders, files in os.walk(input_dir):
		for file in files:
			if not copyToDir(os.path.join(root, file), output_dir):
				print "Unable to move " + file

if __name__ == '__main__':
	main()
