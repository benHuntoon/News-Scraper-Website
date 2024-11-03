# News-Scraper-Website
Online web scraper meant to make searching for news stories easier

LiveLens is a news searching website designed to provide quick access to news articles from a wide variety of trusted sources. Designed to be a student’s best friend, LiveLens is meant to make collecting and citing sources easier than ever. Currently LiveLens is only a prototype, its current features include keyword or source based searches and a database implementation meant to collect user searches for later. As development continues we hope to allow our users the ability to cite sources in a variety of ways, improve the UI, implement a username based account login system, and finally a email/SMS based notification system for updates on stories.

Before running the server we downloaded the mySQL package from pip to connect our data base. To connect the databse this command was used: sudo systemctl start mysql.
Inside the data base I used the sql shell to start running the database using this command: USE news_scraper; (followed by) EXIT;.

The module dependencies not included are flask, mysql-connector, and time. Ensure each of these is installed in the directory before running app.py.

To run LiveLens I created a venv virtual environment on my server and ran the server using this command: nohup python3 app.py

To create a venv on a linux based system, the commands are as follows:
python3 -m venv venv
source venv/bin/activate
pip install Flask

It is important that each html file be place in a directory named template inside of the server. For this current instance style is run out of a project directory on the server, though that is optional, however if that were modified the app.py file would need to be altered as well. The style.css file must be placed in a directory named public for proper functionality. 

The app.py file is the core of the project conencting each branch of the architecture and handling all major processes to be displayed to the user. 

To start the server on local host simply run:
python3 app.py

To start the server remotely run this:
nohup python3 app.py > /dev/null 2>&1 &
