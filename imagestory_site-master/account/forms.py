from django import forms
from .models import *
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.models import User

class MyClearableFileInput(ClearableFileInput):
    initial_text = '현재 사진'
    input_text = '사진 바꾸기'
    clear_checkbox_label = '지우기'

class SignupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'image', 'email',)
        labels = {
            'nickname': '',
            'image': '',
            'email': ''
        }
        widgets = {
            'nickname': forms.TextInput(attrs={
                'id': 'nickname_id',
                'onchange':'rematch(this.id)',
                'placeholder':'닉네임(2글자이상)',
                'required':True,
                'minlength':2,
                'class': 'myname all-line',
                }),
            'email': forms.EmailInput(attrs={
                'id': 'email_id',
                'onchange':"rematch(this.id)",
                'placeholder':'이메일',
                'required':True,
                'class':'myemail all-line',
                }),
            'image': forms.FileInput(attrs={'style':'display:none',})
        }
        error_messages = {
            'nickname': {
                'unique': "중복된 아이디가 존재합니다!",
            },
        }

        onchange="rematch(this.id)"

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password') # 로그인 시에는 유저이름과 비밀번호만 입력 받는다.
        labels = {
            'username': '',
            'password': '',
        }
        help_texts = { 'username': ''}
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder':'아이디',
                'class' :'myusername',
                'style':'text-align:center',
                'required':True,
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder':'비밀번호',
                'class': 'mypassword',
                'style':'text-align:center',
                'required':True,
            }),
        }
        error_messages = {
            'username': {
                'unique': "중복된 닉네임이 존재합니다!",
                'style' : 'color:rgb(234, 140, 140);'
            },
        }

class ModifyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('nickname', 'image', )
        labels = {
            'nickname': '닉네임',
            'image': '프로필 사진',
        }
        widgets = {
            'nickname': forms.TextInput(attrs={'id': 'nickname_id', 'onchange':"rematch(this.id)", }),
            'image': MyClearableFileInput,
        }
        error_messages = {
            'nickname': {
                'unique': "동일한 닉네임이 존재합니다!",
            },
        }

        onchange="rematch(this.id)"