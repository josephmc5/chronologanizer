from datetime import datetime
import re
import os
import exifread
from PIL import Image

class Photo:

    exifTags = None
    fileName = None
    fileHandle = None

    def __init__(self, fileName):
        self.fileName = fileName

    def getFileHandle(self):
        """Returns Image object if successfull"""

        if self.fileHandle:
            return self.fileHandle

        try:
            return Image.open(self.fileName)
        except IOError:
            print("Unable to open image: " + self.fileName)

    def setFileHandle(self, fileHandle):
        self.fileHandle = fileHandle

    def save(self, destination):
        """Takes an Image object and saves it to destination"""

        self.getFileHandle().save(destination, "jpeg", quality = 100)

    def getExifTags(self):

        if self.exifTags:
            return self.exifTags

        f = open(self.fileName, 'rb')
        self.exifTags = exifread.process_file(f)
        return self.exifTags

    def printExifData(self):
        tags = self.getExifTags()

        for tag in tags.keys():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                print("Key: %s, value %s" % (tag, tags[tag]))

    def getDateTaken(self):
        """Returns a date object of the time the picture given was taken."""

        tags = self.getExifTags()

        if 'Image DateTime' in tags:
            # expects format like 2013:11:24 18:38:01
            try:
                return datetime.strptime(str(tags['Image DateTime']),'%Y:%m:%d %H:%M:%S')
            except ValueError:
                return False

    def getOrientation(self):

        tags = self.getExifTags()

        if 'Image Orientation' in tags:
            return str(tags['Image Orientation'])

    def correctOrientation(self):

        orientation = self.getOrientation()

        if not orientation:
            return

        if '180' in orientation:
            self.setFileHandle(self.getFileHandle().rotate(180))
        elif '90' in orientation:
            self.setFileHandle(self.getFileHandle().rotate(-90))
        elif '270' in orientation:
            self.getFileHandle(self.getFileHandle().rotate(-270))

    def resize(self):

        im = self.getFileHandle()
        (width, height) = im.size

        if width > height:
            new_height = 600
            new_width = (600 * width)/height
        else:
            new_width = 600
            new_height = (600 * height)/width

        self.setFileHandle(im.resize((new_width, new_height), Image.ANTIALIAS))

    def isJpeg(self):

        if (not re.match('.jp[e]?g', os.path.splitext(self.fileName)[1], flags=re.IGNORECASE)):
            return False

        return True
    

    def processAndCopy(self,destination_dir):
        """
        Copies the given file into the destination directory with the date structure

        destination directory/year/month/day-time of photo.jpg
        """

        if not self.isJpeg():
            return

        date = self.getDateTaken()

        if not date:
            return

        full_destination_path = os.path.join(destination_dir, date.strftime('%Y'), date.strftime('%m') + "-" + date.strftime('%B'))

        if not os.path.exists(full_destination_path):
            print("Creating " + full_destination_path)
            os.makedirs(full_destination_path)

        self.resize()
        self.correctOrientation()

        save_location = os.path.join(full_destination_path, date.strftime('%B-%d_%I.%M.%S%p.jpg'))
        self.save(save_location)
        return True

