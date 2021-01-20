from django import forms
from .models import *
from django.forms.widgets import ClearableFileInput

class MyClearableFileInput(ClearableFileInput):
    initial_text = '현재 사진'
    input_text = '사진 바꾸기'
    clear_checkbox_label = '지우기'

class Categoryform(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('board_name', 'showing_name', 'ordering','image','cat_image')
        labels = { 'board_name': '게시판아이디', 'showing_name':'게시판이름', 'ordering':'게시판순서', 'image': '게시판이미지', 'cat_image':'게시판아이콘'}
        #help_texts = { 'title': '필수 사항 입니다!', 'body':'내용을 입력해주세요!'}
        widgets = {
            'image': MyClearableFileInput(attrs={'style': 'display:block;margin:auto;'}),
            'cat_image' : MyClearableFileInput(attrs={'style': 'display:block;margin:auto;'}),
            #     'title': forms.TextInput(attrs={'class': 'form-control'}),
            #     'body': forms.Textarea(attrs={'class': 'form-control',}),
        }