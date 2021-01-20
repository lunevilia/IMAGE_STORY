<h1 align="center">이미지스토리 (IMAGESTORY) 🖼</h1>

이미지에 이야기를 남기고, 그 때의 기억을 회상 시킬 수 있는 서비스!

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

## 서비스 주소
**주소 :**<br>
https://www.imagestory.shop/
<br><br>
**이미지스토리 서비스 설명 및 튜토리얼 :**<br>
https://www.imagestory.shop/tutorial/

## 개발자

**👤 이창우**

- Github : https://github.com/cwadven
- Backend : Django
- Service : SQLite, Pythonanywhere
- Server : Pythonanywhere 호스팅<br>(2020-11-05 : Hacker/월 5천원.. DB Mysql할 경우 2만원 훌쩍 ㅠㅠ 그래서 SQLite로 유지중...)
- 기술스택 : Django, JQuery, Imagemapster(오픈라이브러리 : http://www.outsharked.com/imagemapster/)
- 개발기간 : <br>
    - 2020년 6월 29일 ~ 2020 8월 9일 (필수 기능 완성 / 하루에 2시간 씩)
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