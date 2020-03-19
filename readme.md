#! install the virtualenv package on your machine
pip install virtualenv


#! create the virtual env
virtualenv venv

# go to your flask project (from your git bash terminal)
cd Desktop/ENSAM/cours/PJT\ KLEINER/flask_project/

# activate the virtual env
source venv/Scripts/activate


#! install flask package in your virtual env
pip install flask


# set this variable in your machine
set FLASK_APP = run.py


# run the server on default local url : http://127.0.0.1:5000/
python -m flask run


