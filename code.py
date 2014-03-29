#!/usr/bin/python
# code.py
# multi user blog 

import os
import web
import sys

# for absolute paths uncomment below
#import hashlib
#abspath = os.path.dirname(__file__)
#sys.path.append(abspath)
#os.chdir(abspath)

import modelblog 
import blogview
import adminview

urls = (
	'/', 'index',
	'/login/(.*)', 'Login',
	'/private', 'Private',
	'/blog', 'blogview.Blog', 
	'/blogview/(\d+)','blogview.BlogView',
	'/blognew','blogview.BlogNew', 
	'/blogdelete/(\d+)','blogview.BlogDelete',
        '/blogedit/(\d+)','blogview.BlogEdit',
        '/blogadmin','blogview.BlogAdmin',
	'/register','Register',
	'/admin','adminview.Admin'
)

render=web.template.render('templates/')
#render=web.template.render('/var/www/snow365/portal/templates/', base='layout')
db=web.database(dbn='sqlite',db='multi.db')


app = web.application(urls, globals()) 
# uncomment below for sessions management
##application = app.wsgifunc() 
session = web.session.Session(app, 
               web.session.DiskStore('sessions'), 
               initializer={'count': 0}) 

class index:
	def GET(self):
		return render.index()	
class Private: # just a private page example that requires login
        def GET(self):
                web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
		if (mpass !=None and muser !=None): 
			try:
				uauth=db.select('users', where='username=$muser', vars=locals())[0] 
			except:
				return "username does not exist"
		#if mpass == 'dune02': 	# test login without db 
					# remove nested if for single user only 
			if (mpass==uauth.mpassword and muser==uauth.username): 
                        	return render.private() # test redirect
			else:
                        	raise web.seeother('/login/private')
                else:
                        raise web.seeother('/login/private')



#############BEGIN REGISTRATION###############################
class Register:
	register_form = web.form.Form(
		web.form.Textbox("username", description="Username"),
		web.form.Textbox("email", description="E-Mail"),
		web.form.Password("mpassword", description="Password"),
		web.form.Password("password2", description="Repeat password"),
		web.form.Button("submit", type="submit", description="Register"),
		validators = [
		web.form.Validator("Passwords did't match", lambda i: i.mpassword == i.password2)]

	)

	def GET(self):
		f = self.register_form()
		return render.register(f)

	def POST(self):
		f = self.register_form()
        	if not f.validates():
            		return render.register(f)
        	else:
			db.insert('users', username=f.d.username, email=f.d.email, mpassword=f.d.mpassword)
			return """<html>Thanks fo registering <a href="/">home</a>
			</html>"""
            		# do whatever is required for registration
#############END REGISTRATION###############################

class Login:
        def GET(self,site):  
                return render.login(site)
        def POST(self,site):
                # only set cookie if user login succeeds
                mpass = web.input(mpassword=None).mpassword
                muser = web.input(username=None).username
                thesite= web.input(site=None).site 
                if mpass:
                        web.setcookie('mpassword', mpass)
                        web.setcookie('username', muser)
             	raise web.seeother('/%s' % thesite)



#app.add_processor(auth_app_processor)
application = app.wsgifunc()

#uncomment for local testing
if __name__=="__main__":
	app=web.application(urls, globals())
	#app.add_processor(auth_app_processor)
	app.run()
