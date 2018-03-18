# Spoken-Tutorial
Django Application for Spoken Tutorial

# Installation
For linux debian-based system only.

## Django Application
The following are the instructions to install the the application in the workbench to start working.

1. Install Python 3.5 and Pip
    - Debian-Family: `sudo apt install python3.5 python3-pip`
2. Set virtual environment
    1. Make: `python3 -m venv venv`
    2. Activate: `source venv/bin/activate`
3. Install Requirements: `pip3 install -r requirements.txt`
4. Setup Database
    1. Install MySQL: `sudo apt update; sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev python-mysqldb;`
    2. Enter MySQL: `mysql -u root -p`
    3. Create Database: `CREATE DATABASE spoken_tutorial CHARACTER SET UTF8;`
    4. Create User: `CREATE USER spoken_tutorial@localhost IDENTIFIED BY 'MY_AWESOME_PASSWORD';`
    5. Allow User to Access Database: `GRANT ALL PRIVILEGES ON spoken_tutorial.* TO spoken_tutorial@localhost;`
    5. Apply Changes: `FLUSH PRIVILEGES;`
    6. Config Database with django
        1. Open `app/spoken_tutorial/settings.py` and navigate to line `'PASSWORD': 'MY_AWESOME_PASSWORD',` and set your password here.
        2. Inside the virtual environment, run `python3 manage.py makemigrations`
        3. Inside the virtual environment, run `python3 manage.py migrate`
5. Run the server
Inside virtual-environment, run `python3 manage.py runserver`.
Now, go to `127.0.0.1:8000/`, your welcome page should show up.