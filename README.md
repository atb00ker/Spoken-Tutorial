# Spoken-Tutorial

Django Application for Spoken Tutorial

## Installation

For linux debian-based system only.

### Django Application

The following are the instructions to install the the application on a Linux(Debian) Machine.

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
        1. Open `app/spoken_tutorial/settings.py` and navigate to line `'PASSWORD': 'MY_AWESOME_PASSWORD',` and set your password here. Now, inside the virtual environment, run the following commands.
        2.`python3 manage.py makemigrations`
        3.`python3 manage.py migrate`
        4.`python3 manage.py makemigrations portal`
        5.`python3 manage.py migrate portal`
5. Inside virtual-environment, run `python3 manage.py createsuperuser` to create a user that can access the site admin panel.
6. Inside virtual-environment, run `python3 manage.py group` to grant all superusers access to foss admin panel.
7. Run the server: inside virtual-environment, run `python3 manage.py runserver`. Now, go to `127.0.0.1:8000/`, welcome page should show up.
8. Login using the superuser you just created to access the 'Administrator Panel'.
9. You can go to '/admin' when you are logged in from your superuser to make new users and make a user in group 'admin' to allow it to access 'Administration Panel' only.