<h3 align="center">[[홈페이지]]</h3>
<p>
<img alt="imagestory" src="https://github.com/cwadven/imagestory_site/blob/master/asset/imagestory_page.png?raw=true"/>
</p>

<h3 align="center">[[글 목록]]</h3>
<p>
<img alt="imagestory" src="https://github.com/cwadven/imagestory_site/blob/master/asset/imagestory_example2.png?raw=true"/>
</p>

<h3 align="center">[[글 예제]]</h3>
<p>
<img alt="imagestory" src="https://github.com/cwadven/imagestory_site/blob/master/asset/imagestory_example1.png?raw=true"/>
</p>

<h3 align="center">[[마이페이지]]</h3>
<p>
<img alt="imagestory" src="https://github.com/cwadven/imagestory_site/blob/master/asset/imagestory_example3.png?raw=true"/>
</p>
   
   
   
# IMAGE_STORYHO
## 서비스 주소
**주소 :**<br>
http://ghostofsea.pythonanywhere.com/
<br><br>
**이미지스토리 서비스 설명 및 튜토리얼 :**<br>
http://ghostofsea.pythonanywhere.com/tutorial/


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
