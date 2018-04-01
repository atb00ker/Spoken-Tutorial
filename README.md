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

**Note**: You can go to '/admin' when you are logged in from your superuser to make new users and make a user in group 'admin' to allow it to access 'Administration Panel' only.

### Tasks

- ***Task 1***: Database architecture

Also avaiable on [Dropbox Paper](http://bit.do/STModels).

**Note**: More tables than the mentioned tables exists.
Other tables either belong to django or used modules.
The mentioned tables were in the task list, hence mentioned.

#### user

| **Field**      | **Type**     | Null | Key | Default | **Extra**      |
| -------------- | ------------ | ---- | --- | ------- | -------------- |
| id             | int(11)      | No   | PRI | NULL    | auto_increment |
| password       | varchar(128) | No   |     | NULL    |                |
| last_login     | datetime(6)  | Yes  |     | NULL    |                |
| is_superuser   | tinyint(1)   | No   |     | NULL    |                |
| username       | varchar(150) | No   | UNI | NULL    |                |
| first_name     | varchar(30)  | No   |     | NULL    |                |
| last_name      | varchar(150) | No   |     | NULL    |                |
| email          | varchar(254) | No   |     | NULL    |                |
| is_staff       | tinyint(1)   | No   |     | NULL    |                |
| is_active      | tinyint(1)   | No   |     | NULL    |                |
| date_joined id | datetime(6)  | No   |     | NULL    |                |

#### foss

| **Field** | **Type**     | Null | Key | Default | **Extra**      |
| --------- | ------------ | ---- | --- | ------- | -------------- |
| foss_id   | int(11)      | NO   | PRI | NULL    | auto_increment |
| title     | varchar(250) | NO   |     | NULL    |                |
| user_id   | int(11)      | YES  |     | NULL    |                |

#### tutorial_detail

| **Field**                | **Type**     | Null | Key | Default | **Extra**      |
| ------------------------ | ------------ | ---- | --- | ------- | -------------- |
| tut_id                   | int(11)      | NO   | PRI | NULL    | auto_increment |
| actual_submission_date   | datetime(6)  | YES  |     | NULL    |                |
| expected_submission_date | datetime(6)  | NO   |     | NULL    |                |
| is_published             | tinyint(1)   | NO   |     | NULL    |                |
| title                    | varchar(250) | NO   |     | NULL    |                |
| assigned_by_id           | int(11)      | NO   | MUL | NULL    |                |
| foss_id                  | int(11)      | NO   | MUL | NULL    |                |

#### payment

| **Field**      | **Type**    | Null | Key | Default | **Extra**      |
| -------------- | ----------- | ---- | --- | ------- | -------------- |
| id             | int(11)     | NO   | PRI | NULL    | auto_increment |
| amount         | int(11)     | NO   |     | NULL    |                |
| date           | datetime(6) | NO   |     | NULL    |                |
| approved_by_id | int(11)     | NO   | MUL | NULL    |                |
| payment_for_id | int(11)     | NO   | MUL | NULL    |                |

**Note**: The following information is also available on [paper](http://bit.do/STInfo)

#### **Create Users**

When you Login from the superuser account you can create new users. These users may or may not be administrators and you can control their group by putting them in the ‘admin’ group or not.

#### **Administrator Panel**

![Admin Panel](https://d2mxuefqeaa7sj.cloudfront.net/s_A6509E00434CBFE85F845312F00EB04E36C43890CCE73C9C71D5171BE61B1945_1522142164041_admin+panel.png)

When you login with the user account that is in Admin group, you get to see “Admin Panel” in the options on the header bar.
The Admin Panel 3 options.

1. FOSS
2. Submissions
3. Payment

#### **FOSS**

![figure(i)](https://d2mxuefqeaa7sj.cloudfront.net/s_A6509E00434CBFE85F845312F00EB04E36C43890CCE73C9C71D5171BE61B1945_1522141638023_tut.png)

View all the foss and tutorials, or create new foss and tutorials from the view.
You can also mark the foss as submitted. After the foss is submitted, it can be published.

#### **Submissions**

![figure (ii)](https://d2mxuefqeaa7sj.cloudfront.net/s_A6509E00434CBFE85F845312F00EB04E36C43890CCE73C9C71D5171BE61B1945_1522141638009_publish.png)

- ***Task 2:*** The list of all the contributed foss for a selected month as shown in the table. See *figure (ii)*, you can mark a foss submitted from this table.

#### **Payment**

![figure (iii)](https://d2mxuefqeaa7sj.cloudfront.net/s_A6509E00434CBFE85F845312F00EB04E36C43890CCE73C9C71D5171BE61B1945_1522141638000_calc.png)

- ***Task 3:*** This table shows data only for the published foss in the selected month.
- ***Task 4:*** The Payment table contains the amount to the paid to the contributor.
- ***Task 5:*** The table of the users to be paid for a month is displayed in the *figure (iii)*.

### **Why is admin group used?**

Admin group has the permission to change the FOSS information and superuser has all the permissions.
This is done so that admins with limited power can be easily created if there is  a need for the same.

![Site Administrator](https://d2mxuefqeaa7sj.cloudfront.net/s_A6509E00434CBFE85F845312F00EB04E36C43890CCE73C9C71D5171BE61B1945_1522141638028_users.png)
