from django.db import models



# from django.conf import settings
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File

from django.urls import reverse
# from django.core.urlresolvers import reverse


# Create your models here.
class Category(models.Model):
    board_name = models.CharField(max_length=50, unique=True) # 백엔드에서 식별하기 위해 쓰는 것
    showing_name = models.CharField(max_length=50,) # 사용자들에게 보여주는 것
    ordering = models.FloatField()
    image = models.ImageField(upload_to='cat_picture/', null=True, blank=True)
    cat_image = models.ImageField(upload_to='cat_icon/', null=True, blank=True)

    def __str__(self):
        return self.board_name

    def save(self, *args, **kwargs): #저장할때 이미지는 orientation 맞춰서 저장 또한 전부 삭제 exif정보
        if self.image:
            pilImage = Img.open(BytesIO(self.image.read()))
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = dict(pilImage._getexif().items())

                if exif[orientation] == 3:
                    pilImage = pilImage.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    pilImage = pilImage.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    pilImage = pilImage.rotate(90, expand=True)

                output = BytesIO()
                pilImage.save(output, format='JPEG', quality=75)
                output.seek(0)
                self.image = File(output, self.image.name)
            except:
                pass

        return super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-ordering']