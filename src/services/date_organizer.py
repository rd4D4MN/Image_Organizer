from datetime import datetime
import os
from PIL import Image
from PIL.ExifTags import TAGS

class DateOrganizer:
    def __init__(self, images):
        self.images = images

    def organize_by_date(self):
        organized_images = {}
        for image in self.images:
            creation_date = self.get_creation_date(image)
            year = creation_date.year
            month = creation_date.month
            
            if year not in organized_images:
                organized_images[year] = {}
            if month not in organized_images[year]:
                organized_images[year][month] = []
                
            organized_images[year][month].append(image)
        
        return organized_images

    def get_creation_date(self, image):
        """Extract date from image using EXIF data or file creation time."""
        try:
            # Try to get EXIF data
            exif = image._getexif()
            if exif:
                # Look for DateTimeOriginal or DateTime tag
                for tag_id in exif:
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in ['DateTimeOriginal', 'DateTime']:
                        date_str = exif[tag_id]
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')

            # If no EXIF data, try to get file creation time
            if hasattr(image, 'filename'):
                timestamp = os.path.getctime(image.filename)
                return datetime.fromtimestamp(timestamp)
            
            # If all else fails, use current date
            return datetime.now()

        except Exception as e:
            print(f"Warning: Could not get date for image, using current date. Error: {e}")
            return datetime.now()