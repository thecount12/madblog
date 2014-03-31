# madblog
=======

Simple multi user blog written in python using webpy framework

you can use any theme such as boilerplate, bootstrap, 960.gs, skeleton-gs etc...

----

Check out notes.txt for additional details and todo:

1. download master.zip and make sure following dependencies are installed 
	- sudo apt-get install python-webpy
	- sudo apt-get install sqlite3

2. run setup script to create schema.sql and populate multi.db: ./setup.sh 
	- don't forget to change username and password for admin user

3. start web framework: ./run.sh 
	- don't forget to change ip address and port

4. Contact page uses pvgmail.py 
	- change username and password in that file 
