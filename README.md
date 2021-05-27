# IMAGE_STORYHO

http://ghostofsea.pythonanywhere.com/


환경 구축
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
