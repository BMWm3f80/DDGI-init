# DDGI-automation-back
python >=3.5
pip install requirements.txt



Run in CMD:
    * Got to dir that contains manage.py file
    * in cmd run: python manage.py runserver 0.0.0.0
    
In your broeswer:
    * 127.0.0.1:8000/admin     admin panle Django
    * 127.0.0.1:8000/api/token/    access token handler
    * 127.0.0.1:8000/test/         custom test handler, returns username if jwt-auth is successful
