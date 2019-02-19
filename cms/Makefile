install:
	pip install -qr requirements/development.txt --exists-action w
populate:
	python manage.py populate_data -f learning_outcomes/management/commands/input.csv
migrate:
	python manage.py migrate
run:
	python manage.py runserver