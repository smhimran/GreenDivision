release: python manage.py migrate && python manage.py problem_populate
web: gunicorn GreenDivision.wsgi --log-file -