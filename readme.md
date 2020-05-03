# go to your project  

## go to your flask project (from your git bash terminal)  
cd ...


# Virtual Environement Setting  

## ! install the virtualenv package on your machine   
pip install virtualenv

##! create the virtual env   
virtualenv venv

## (linux) activate the virtual env   
source venv/Scripts/activate

## (windows) activate the virtual env   
venv\Scripts\activate

## ! install flask package in your virtual env   
pip install flask


# Run the server

## (linux) set this variable in your machine  
export FLASK_APP=run.py

## (windows) set this variable in your machine  
set FLASK_APP = run.py

## (linux) run the server on default local url : http://127.0.0.1:5000/  
flask run

## (windows) run the server on default local url : http://127.0.0.1:5000/  
python -m flask run



# Git Usage

!! always set yourself at the root of your project

## Push Process
git add .   
git commit -m "your message"   
git push   

## Pull Process
git pull

