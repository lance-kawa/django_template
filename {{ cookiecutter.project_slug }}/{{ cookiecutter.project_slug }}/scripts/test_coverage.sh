# we want the tests to crash if they fail
coverage run manage.py test  || { echo 'tests failed' ; exit 1; }

# otherwise, we generate the different outputs
coverage report
coverage xml -o /home/backend/coverage/coverage.xml
coverage html -d /home/backend/coverage/htmlcov
