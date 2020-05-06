pip3 install virtualenv
virtualenv venv
source venv/bin/activate
pip3 install flask flask-graphql flask-migrate flask-sqlalchemy graphene graphene-sqlalchemy
python3 uwsgi.py