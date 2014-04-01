# madblog
=======

Simple multi user blog written in python using webpy.org framework.
You can use any theme such as boilerplate, bootstrap, 960.gs, skeleton-gs etc...

----

Check out notes.txt for additional details and todo:

1. download master.zip and make sure following dependencies are installed 
	- sudo apt-get install python-webpy
	- sudo apt-get install sqlite3

2. run setup script to create schema.sql and populate multi.db: ./setup.sh 
	- don't forget to change username and password for admin user

3. start web framework: ./run.sh 
	- don't forget to change ip address and port in that file 

4. Contact page uses pvgmail.py 
	- change username and password in that file

----

CHANGE THEMES

1. edit code.py and look for:
	- render=web.template.render('templates/')
	- render=web.template.render('templates/', base='layout') # layout.html
	- admrender=web.template.render('templates/', base='adminlayout')#adminlayout.html
	- render=web.template.render('templates/', base='layout960') # layout960.html


Changing "render" variable changes how or where html files are rendered 
in the template directory it also affects each "class method object" and how
it's rendered. For instance: 

	render=web.template.render('templates/', base='layout') # layout.html
	brender=web.template.render('templates/', base=layout2') # layout2.html 
	class Test:
		def GET(self):
			return render.test() # /templates/test.html
	class Test2
		def GET(self)
			return brender.test2() # /templates/test2.html

Both variables for "render" and "brender" are uncommented and can be used
for each "class" object with different layouts. The "base='layout'" allows
you to utilize a header, footer, and stylesheet on all pages.	

Here is an example of layout.html:

 
	$def with (content)
	<html>
	<head>
	<title>madblog simple multi-user python blog</title>
	</head>
	<body>
		<!-- header begin -->
	<h2>madblog</h2>
	<center>
	<p><a href="/">Home</a> | 
	<a href="/blog">Blog</a> | 
	<a href="/contact">Contact</a> | 
	<a href="/register">Register</a> | 
	<a href="/login/">Login</a> |
	<a href="/logout">Logout</a>  
	</center>
	<hr>
		<!-- header end --> 
		<!-- main content begin # notice dollar sign :content-->
	$:content
		<!-- main content end-->
		<!-- footer begin -->
	<hr>
	<center> &copy; www.domain.com</center>
		<!-- footer end -->
	</body>
	</html>

2. changing html files and adding new pages. All html files exist in /templates 
directory. However you need to modify code.py to make them appear. Here is
an example of adding a new page:

	urls=(
		'/newpage','Newpage'
	)
	class Newpage
		def GET(self):
			return render.newpage(): 	

newpage.html should exist in /templates directory  
 
