# Spoken-Tutorial

Django Application for Spoken Tutorial

## Installation

For linux debian-based system only.

### Django Application

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
    6. Apply Changes: `FLUSH PRIVILEGES;`
    7. Config Database with django
        1. Open `app/spoken_tutorial/settings.py` and navigate to line `'PASSWORD': 'MY_AWESOME_PASSWORD',` and set your password here.
        2. Inside the virtual environment, run `python3 manage.py makemigrations`
        3. Inside the virtual environment, run `python3 manage.py migrate`
5. Run the server: inside virtual-environment, run `python3 manage.py createsuperuser` to create a user that can access the admin panel.
6. Run the server: inside virtual-environment, run `python3 manage.py runserver`. Now, go to `127.0.0.1:8000/`, welcome page should show up.
7. Login using the superuser you just created to access the 'Administrator Panel'.
8. You can go to '/admin' when you are logged in from your superuser to make new users and make a user in group 'admin' to allow it to access 'Administration Panel' only.