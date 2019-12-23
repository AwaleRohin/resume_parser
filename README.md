# resume_parser
### Simple Resume Parser

## Steps to run project
- First make sure you have python install along with pip and virtualenv. Usually pip is installed along python and to install virtualenv: pip install virtualenv
- clone the repo 
- create virtualenv: ```virtualenv venv``` or ```virtualenv -p python3 venv```
- activate virtualenv: for linux(```source venv/bin/activate```) and for windows(```source venv/Scripts/activate```)
- install django and necessary libraries in venv: ```pip install -r requirements.txt``` (all necessary libraries for project are in requirements.txt file) 
- also install ```python -m spacy download en_core_web_sm```
- before migrating make sure that you have install postgresql in your computer and if you want to use sqlite change the database in settings
- make neccessary migrations : ```python manage.py makemigrations```
- migrate the files: ```python manage.py migrate```
- create one superuser to access the admin panel: ```python manage.py createsuperuser```
- finally run the project: ```python manage.py runserver```
