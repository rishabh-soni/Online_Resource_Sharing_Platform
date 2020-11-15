# ![Unable to load image](https://github.com/rishabh-soni/Online_Resource_Sharing_Platform/blob/master/static/images/logohorizontal.png?raw=true) 
## Online Resource Sharing Platform

HoneyComb is an interactive platform for buying, selling, and renting any students' resources within the IITI community. The web application's closure to IITI students would provide a better platform for students to share their belongings. Students can sell or rent their notes, books, stationeries, furniture, and much more.
The project is made using **django** while **MySQL** is used for database management.

Visit our website [here](http://honeycombiiti.pythonanywhere.com) or alternatively by clicking on the link http://honeycombiiti.pythonanywhere.com

## Project Requirements (for local hosting)
* Python 3.8
* MySQL server and MySQL Workbench (recommended 8.0 and above)
* Git

### To run the project on local server,
* Clone the remote reopsitory on your system.
* Install all the dependencies by running the command **pip install -r requirements.txt**
* Create a new connection in MySQL Workbench and import the database from database.sql file in the **/sqldump** directory.
* Run the command **python manage.py makemigrations**
* Run the command **python manage.py migrate**
* Run the command **python manage.py runserver** and browse the corresponding URL provided.
