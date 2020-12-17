#!/usr/bin/env python
"""
Chronologanizer is a simple script to organize your pictures based on
the year, month, date, and time it was taken.

Joe McWilliams <github@joemcwilliams.com>
"""

import argparse
import os
import sys
from Photo import Photo

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', default='.')
    parser.add_argument('-o', '--output', default='/tmp/')
    args = parser.parse_args()

    input_dir = os.path.normpath(os.path.expanduser(args.input))
    output_dir = os.path.normpath(os.path.expanduser(args.output))

    if (not os.path.exists(input_dir)):
        print("Input path does not exist: " + input_dir)
        sys.exit(1)


    print("Looking for pictures in " + input_dir)

    for root, subFolders, files in os.walk(input_dir):
        for file in files:
            myPhoto = Photo(os.path.join(root, file))
            if not myPhoto.processAndCopy(output_dir):
                print("Skipping " + file)

if __name__ == '__main__':
    main()
