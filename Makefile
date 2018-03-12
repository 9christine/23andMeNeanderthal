all:
	pip install -r requirements.txt
	./manage.py migrate

test:
	./manage.py test

run:
	./manage.py runserver

.PHONY: test run
