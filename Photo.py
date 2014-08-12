from datetime import datetime
import re
import os
import exifread
from PIL import Image

class Photo:

    exifTags = None
    fileName = None

    def __init__(self, fileName):
        self.fileName = fileName

    def getExifTags(self):

        if self.exifTags:
            return exifTags

        f = open(self.fileName, 'rb')
        self.exifTags = exifread.process_file(f)
        return self.exifTags

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

        if 'Orientation' in tags:
            return str(tags['Orientation'])

    def resize(self,destination):

        try:
            im = Image.open(self.fileName)
            (width, height) = im.size

            if width > height:
                new_height = 600
                new_width = (600 * width)/height
            else:
                new_width = 600
                new_height = (600 * height)/width

            im = im.resize((new_width, new_height), Image.ANTIALIAS)
            im.save(destination, "jpeg", quality = 100)
        except IOError:
            print "Unable to resize image: " + self.fileName

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
            print "Creating " + full_destination_path
            os.makedirs(full_destination_path)

        self.resize(os.path.join(full_destination_path, date.strftime('%B.%d-%I.%M.%S%p.jpg')))

        return True

