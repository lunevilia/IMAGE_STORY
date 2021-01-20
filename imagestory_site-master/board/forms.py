from django import forms
from .models import *
from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial_text = '현재 사진'
    input_text = '사진 바꾸기'
    clear_checkbox_label = '지우기'

class Boardmodform(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'information', 'important', 'image', 'cord_sx', 'cord_sy', 'cord_lx', 'cord_ly', 'secure',)
        labels = {
            'title': '제목',
            'information':'내용',
            'important':'중요도',
            'image':'이미지',
            'secure':'공개유무',
            'cord_sx':'',
            'cord_sy':'',
            'cord_lx':'',
            'cord_ly':'',
        }
        error_messages = {
            'secure': {
                'required': "공개유무를 선택해주세요!",
            },
        }
        help_texts = { 'image':'1MB 이상 이미지는 올릴 수 없습니다.', }
        widgets = {
            'cord_sx':forms.NumberInput(attrs={'style': 'display:none'}),
            'cord_sy':forms.NumberInput(attrs={'style': 'display:none'}),
            'cord_lx':forms.NumberInput(attrs={'style': 'display:none'}),
            'cord_ly':forms.NumberInput(attrs={'style': 'display:none'}),
            'image': MyClearableFileInput(attrs={'style': 'display:block;margin:auto;'}),
            'title': forms.TextInput(attrs={'class': 'mytitle'}),
            'information': forms.Textarea(attrs={'class': 'mybody',}),
        }
        
class Boardmodform_root(forms.ModelForm):
    class Meta:
        model = Board
        fields = ('title', 'information', 'image', 'secure')
        labels = {
            'title': '제목',
            'information':'내용',
            'image':'이미지',
            'secure':'공개유무',
        }
        help_texts = { 'image':'1MB 이상 이미지는 올릴 수 없습니다.', }
        widgets = {
            'image': MyClearableFileInput(attrs={'class': 'upload-hidden', "id":"input-file", "type":"file"}),
            'title': forms.TextInput(attrs={'class': 'mytitle', "placeholder" : '입력해주세요.'}),
            'information': forms.Textarea(attrs={'class': 'mybody', "placeholder" : '내용을 입력해주세요.'}),
            'secure' : forms.Select(attrs={'class': "myscure"}),
        }
        
class CommentTest(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        labels = { 'body': '',}
        widgets = {
            'body': forms.TextInput(attrs={
                'class': 'form-control', 
                'rows':3,
                'id':False,
                'placeholder':'의견작성',
                'style':'font-size: 1.7ch;'
                }),
        }
