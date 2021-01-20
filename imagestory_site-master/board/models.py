from django.db import models
from category.models import Category
from account.models import Profile

# from django.conf import settings
from PIL import Image as Img
from PIL import ExifTags
from io import BytesIO
from django.core.files import File

from django.urls import reverse
# from django.core.urlresolvers import reverse

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class Board(TimeStampedModel):

    secure_options = [
        ('public', '공개'),
        ('private', '비공개'),
    ]

    #탈퇴 회원 글 남겨 놓도록 하기
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    secure = models.CharField(max_length=7, choices=secure_options)
    title = models.CharField(max_length=50)
    information = models.TextField()
    cord_sx = models.IntegerField(null=True, blank=True)
    cord_sy = models.IntegerField(null=True, blank=True)
    cord_lx = models.IntegerField(null=True, blank=True)
    cord_ly = models.IntegerField(null=True, blank=True)
    important = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='board_picture/', null=True, blank=True)
    post = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    post_root = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="root")

    group = models.ManyToManyField(Profile, blank=True, related_name="group")

    class Meta:
        ordering = ['-important']

    def __str__(self):
        return self.title

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
                pilImage.save(output, format='JPEG', quality=100)
                output.seek(0)
                self.image = File(output, self.image.name)
            except:
                pass

        return super(Board, self).save(*args, **kwargs)

    def short_title(self):
        if len(self.title)>15:
            return self.title[:15]+"..."
        else:
            return self.title

    # 경로 보여주기에서 사용되는 이름 짧게 만들기
    def route_title(self):
        if len(self.title)>4:
            return self.title[:4]+".."
        else:
            return self.title

    def short_information(self):
        if len(self.information)>25:
            return self.information[:25]+"..."
        else:
            return self.information

    def show_all_node(self):
        note = self
        show = ""
        while note.post is not None:
            note = note.post
            show = str(note.title) + " > " + show
        return show

    #sitemap 생성하기 위해서 reverse를 사용하여 해당 매개변수를 넣기
    def get_absolute_url(self):
        try:
            return reverse('board:detail', kwargs={'id':self.id, 'board_name':self.category.board_name })
        except:
            pass

class Comment(TimeStampedModel):
    main_post = models.ForeignKey(Board, on_delete=models.CASCADE)
    post = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    body = models.TextField()

    def __str__(self):
        return '%s - %s - %s' % (self.main_post, self.post, self.body)

    def natural_key(self): #json serialize 에서 특정 내용만 가져오기 위해서 설정 원래는 pk 정보만 나오는데 이렇게 설정
        return (self.body)

#알람 내용
class Commentalertcontent(TimeStampedModel):
    profile_name = models.ForeignKey(Profile, on_delete=models.CASCADE) # models.CharField(max_length=300)
    sender_name = models.CharField(max_length=300)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    content = models.ForeignKey(Comment, on_delete=models.CASCADE)
    view = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id', ]

    def __str__(self):
        return '%s - %s - %s' % (self.profile_name.nickname, self.board, self.content)

    def natural_key(self): #json serialize 에서 특정 내용만 가져오기 위해서 설정 원래는 pk 정보만 나오는데 이렇게 설정
        return (self.content)

class Bookmark(TimeStampedModel):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    post = models.ForeignKey(Board, on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.post)
