# tornado-challenger
Web-application that uses Python, Tornado and MongoDB.

Here you can create new challenges, record them, motivate yourself and just improve your skills.
Challenge - is the endpoint, which you want to achieve, and this application gives you interface to 
manage them.

You can for example create challenge - Learn Tornado in a Week, then create Points, which you want to do
during this challenge, for instance Read som book about Tornado and create some project. You can then 
determine how much time you need to do that and save it. It works like to-do list.

This project is written in pure Tornado, as database MongoDB and drive mongoengine are used.

To install this software on Linux:
- most important thing: you need to put this software into virtualenv with python3 distribution, to do this enter following commands : sudo apt-get install python-virtualenv; virtualenv --no-packages --distributive -p /ust/local/lib/python3.4 <name_of_virtualenv>; then out all the files into this folder and activate virtualenv, entering in virtualenv folder command source bin/activate; then follow next steps;
- install MongoDB http://docs.mongodb.org/manual/administration/install-on-linux/   - choose your Linux system and follow steps;
- install requirements.txt with command pip install -r requirements.txt (of course you need to have python3 and pip3 pre installed on your os);
- after installing MongoDB run file db.py, which will create database on your system;
- in the directory of your project run command python challenge_manager.py;
- everything has to work, if previous steps were fulfilled properly, now enter following url in your browser http://127.0.0.1:8000, you should see home page of the project;
