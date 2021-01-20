from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=16, unique=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    email = models.EmailField(null=True, blank=False, unique=True)
    alert = models.IntegerField(default=0)

    def __str__(self):
        return self.nickname
    
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

        return super(Profile, self).save(*args, **kwargs)

class Commentalert(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    recent = models.IntegerField(default=0)

    def __str__(self):
        return '%s - %s' % (self.profile.nickname, self.recent)