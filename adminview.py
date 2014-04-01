import web
from datetime import datetime

urls=(
        "","anything",
        "/admin","Admin", 
	"/adminuser","AdminUser",
	"/adminusernew","AdminUserNew",
	"/adminuserdelete/(\d+)","AdminUserDelete",
	"/adminuseredit/(\d+)","AdminUserEdit"
)

#render=web.template.render('templates/')
#render=web.template.render('templates/', base='layout')
render=web.template.render('templates/', base='layout960') # layout960.html 
admrender=web.template.render('templates/', base='adminlayout')#adminlayout.html
db=web.database(dbn='sqlite',db='multi.db')


class anything: #important path back to code.py or root
        def GET(self): raise web.seeother('/')

##########BEGIN ADMIN SECTION################

class Admin: # just a private page example that requires login
        def GET(self): # extracted from private
                web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
                if (mpass !=None and muser !=None):
                        try:
                                uauth=db.select('users', where='username=$muser', vars=locals())[0]
                        except:
                                return "username does not exist"
                #if mpass == 'dune02':  # test login without db
                                        # remove nested if for single user only
                        if (mpass==uauth.mpassword and muser==uauth.username and uauth.admin=="Yes"):
                                return admrender.admin() # test redirect
                        else:
                                raise web.seeother('/login/admin')
                else:
                        raise web.seeother('/login/admin')

class AdminUser:
	def GET(self):
		web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
                if (mpass !=None and muser !=None):
                        try:
                                uauth=db.select('users', where='username=$muser', vars=locals())[0]
                        except:
                                return "username does not exist"
                #if mpass == 'dune02':  # test login without db
                                        # remove nested if for single user only
                        if (mpass==uauth.mpassword and muser==uauth.username and uauth.admin=="Yes"):
				luser=db.select("users", order='id DESC') 
                                return admrender.adminuser(luser) # test redirect
                        else:
                                raise web.seeother('/login/adminuser')
                else:
                        raise web.seeother('/login/adminuser')

class AdminUserNew:
        form = web.form.Form(
                web.form.Textbox('username', web.form.notnull,
                        size=30,
                        description="Username:"),
                web.form.Password('mpassword', web.form.notnull,
                        size=30,
                        description="Password:"),
                web.form.Textbox('email', web.form.notnull,
                        size=20,
                        description="Email:"),
                web.form.Textbox('hint', web.form.notnull,
                        size=20,
                        description="Hint:"),
                web.form.Textbox('admin', web.form.notnull,
                        size=20,
			value="No",
                        description="Admin:"),
                web.form.Textbox('author', web.form.notnull,
                        size=20,
			value="No",
                        description="Author:"),
                web.form.Textbox('view', web.form.notnull,
                        size=20,
			value="No",
                        description="View:"),
                web.form.Textbox('date', web.form.notnull,
                        size=20,
			value=(str(datetime.now())),
                        description="Date:"),
                web.form.Button('Post entry'),
                )
        def GET(self):
                web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
                if (mpass !=None and muser !=None):
                        try:
                                uauth=db.select('users', where='username=$muser', vars=locals())[0]
                        except:
                                return "username does not exist or you have been logged out"
                        if (mpass==uauth.mpassword and muser==uauth.username and uauth.admin=="Yes"):
                                form=self.form()
                                return admrender.adminusernew(form)
                        else:
                                raise web.seeother('/login/adminusernew')
                else:
                        raise web.seeother('/login/adminusernew')
        def POST(self):
                form = self.form()
                if not form.validates():
                        return admrender.adminusernew(form)
                db.insert('users', username=form.d.username, mpassword=form.d.mpassword, email=form.d.email, hint=form.d.hint, admin=form.d.admin, author=form.d.author,view=form.d.view,date=form.d.date)
                raise web.seeother('/adminuser')



class AdminUserDelete:
        def POST(self, id):
		db.delete('users', where="id=$id", vars=locals())
                raise web.seeother('/adminuser')
class AdminUserEdit:
        def GET(self, id):
                web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
                if (mpass !=None and muser !=None):
                        try:
                                uauth=db.select('users', where='username=$muser', vars=locals())[0]
                        except:
                                return "username does not exist"
                        if (mpass==uauth.mpassword and muser==uauth.username and uauth.admin=="Yes"):
                                luser= db.select('users', where='id=$id', vars=locals())[0]
                                form =AdminUserNew.form()
                                form.fill(luser)
                                return admrender.adminuseredit(luser, form)
                        else:
                                raise web.seeother('/login/blogedit/%s' % id)
                else:
                        raise web.seeother('/login/blogedit/%s' % id)



        def POST(self, id):
                form = AdminUserNew.form()
                luser= db.select('users', where='id=$id', vars=locals())[0]
                if not form.validates():
                        return admrender.adminuseredit(luser, form)
		db.update('users', where="id=$id", vars=locals(),
                username=form.d.username, mpassword=form.d.mpassword, email=form.d.email, hint=form.d.hint, admin=form.d.admin, author=form.d.author,view=form.d.view,date=form.d.date)
                raise web.seeother('/adminuser')

