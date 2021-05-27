<h1 align="center">이미지스토리 (IMAGESTORY) 🖼</h1>

이미지에 이야기를 남기고, 그 때의 기억을 회상 시킬 수 있는 서비스!

<h3 align="center">[[홈페이지]]</h3>
<p align="center">
<img alt="imagestory" src="https://github.com/lunevilia/IMAGE_STORY/blob/main/imagestory_site-master/asset/imagestory_example1.PNG?raw=true"/>
</p>

<h3 align="center">[[회원가입]]</h3>
<p align="center">
<img alt="imagestory" src="https://github.com/lunevilia/IMAGE_STORY/blob/main/imagestory_site-master/asset/imagestory_example3.PNG?raw=true"/>
</p>

<h3 align="center">[[글 예시1]]</h3>
<p  align="center">
<img alt="imagestory" src="https://github.com/lunevilia/IMAGE_STORY/blob/main/imagestory_site-master/asset/imagestory_example2.PNG?raw=true"/>
</p>

<h3 align="center">[[글 예시2]]</h3>
<p align="center">
<img alt="imagestory" src="https://github.com/lunevilia/IMAGE_STORY/blob/main/imagestory_site-master/asset/imagestory_example4.PNG?raw=true"/>
</p>

## 서비스 주소
**주소 :**<br>
http://ghostofsea.pythonanywhere.com/
<br><br>
**이미지스토리 서비스 설명 및 튜토리얼 :**<br>
http://ghostofsea.pythonanywhere.com/tutorial/
## 서브개발자

- 개발기간 : <br>
    - 2020년 8월 9일 ~ 지금 (필요에 따른 유지보수)

## 환경 구축

~~~
1. python -m venv myvenv (가상환경 생성)
2. python source myvenv/Script/activates (가상환경 실행)
3. pip install -r requirements.txt (의존성 모듈 설치)
4. python manage.py collectstatic (static 파일 생성)
5. python manage.py makemigrations account
6. python manage.py makemigrations category
7. python manage.py makemigrations board
8. python manage.py migrate (테이블 생성)
9. python manage.py createsuper (관리자 id 생성)
10. python manage.py runserver
~~~
