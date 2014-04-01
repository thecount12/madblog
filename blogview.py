import web
import modelblog
from datetime import datetime

urls=(
	"","anything",
	"/blog","Blog",
	'/blogview/(\d+)','BlogView', 
	'/blognew','BlogNew',
	'/blogspecial','BlogSpecial',
	'/blogdelete/(\d+)','BlogDelete',
        '/blogedit/(\d+)','BlogEdit',
        '/blogadmin','BlogAdmin'

)

#render=web.template.render('templates/')
admrender=web.template.render('templates/', base='adminlayout')#adminlayout.html
#render=web.template.render('templates/', base='layout')
render=web.template.render('templates/', base='layout960') # layout960.html 
db=web.database(dbn='sqlite',db='multi.db')


class anything: #important path back to code.py or root 
	def GET(self): raise web.seeother('/')

############ BEGIN BLOG########################
class Blog:
        def GET(self):
                """ Show page """
                posts = modelblog.get_posts()
                return render.blog(posts)
class BlogView:
        def GET(self, id):
                """ View single post """
                post = modelblog.get_post(int(id))
                web.header('Content-Type','text/html')
                return render.blogview(post)
class BlogNew:
        form = web.form.Form(
                web.form.Textbox('author', web.form.notnull,
                        size=30,
                        description="Author:"),
                web.form.Textbox('title', web.form.notnull,
                        size=30,
                        description="Post title:"),
                web.form.Textbox('date', web.form.notnull,
                        size=20,
			value=(str(datetime.now())),
                        description="Date:"),
		web.form.Hidden('approved', web.form.notnull,
			value="No"),
		web.form.Hidden('published', web.form.notnull,
			value="No"),
                web.form.Textarea('content', web.form.notnull,
                        rows=30, cols=80,
                        description="Post content:"),
                web.form.Button('Post entry'),
                )
        def GET(self):
		web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
		if (mpass !=None and muser !=None): 
			try:
				uauth=db.select('users', where='username=$muser', vars=locals())[0] 
			except:
				return "username does not exist"
			if (mpass==uauth.mpassword and muser==uauth.username and uauth.author=="Yes"): 
				form=self.form() 
				return render.blognew(form)
			else:
				#raise web.seeother('/login/blognew')
				return """<html>Your account needs to be approved to make posts
					<p>or password is incorrect:<a href="/login/blognew">try again</a></html>
				"""
                else:
                        raise web.seeother('/login/blognew')
        def POST(self):
      		web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
		form = self.form()
                if not form.validates():
                        return render.blognew(form)
                #modelblog.new_post(form.d.title, form.d.author, form.d.content, form.d.date)
		db.insert('blog', title=form.d.title, author=form.d.author, content=form.d.content, date=form.d.date, approved=form.d.approved, published=form.d.published ,username=muser)
                raise web.seeother('/blog')

class BlogSpecial:
        form = web.form.Form(
                web.form.Textbox('author', web.form.notnull,
                        size=30,
                        description="Author:"),
                web.form.Textbox('title', web.form.notnull,
                        size=30,
                        description="Post title:"),
                web.form.Textbox('date', web.form.notnull,
                        size=20,
			value=(str(datetime.now())),
                        description="Date:"),
		web.form.Textbox('approved', web.form.notnull,
			size=20,
			value="Yes",
			description="Approved:"),
		web.form.Textbox('published', web.form.notnull,
			size=20,
			value="Yes",
			description="Published:"),
                web.form.Textarea('content', web.form.notnull,
                        rows=30, cols=80,
                        description="Post content:"),
                web.form.Button('Post entry'),
                )
        def GET(self):
		web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
		if (mpass !=None and muser !=None): 
			try:
				uauth=db.select('users', where='username=$muser', vars=locals())[0] 
			except:
				return "username does not exist"
			if (mpass==uauth.mpassword and muser==uauth.username and uauth.admin=="Yes"): 
				form=self.form() 
				return admrender.blogspecial(form)
			else:
                        	raise web.seeother('/login/blogspecial')
                else:
                        raise web.seeother('/login/blogspecial')
        def POST(self):
		web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
                form = self.form()
                if not form.validates():
                        return admrender.blognewspecial(form)
                #modelblog.new_post(form.d.title, form.d.author, form.d.content, form.d.date)
		db.insert('blog', title=form.d.title, author=form.d.author, content=form.d.content, date=form.d.date, approved=form.d.approved, published=form.d.published,username=muser )
                raise web.seeother('/blogadmin')



class BlogDelete:
        def POST(self, id):
                modelblog.del_post(int(id))
                raise web.seeother('/blogadmin')
class BlogEdit:  
        def GET(self, id):
                web.ctx.mpassword = mpass = web.cookies(mpassword=None).mpassword
                web.ctx.username = muser = web.cookies(username=None).username
		if (mpass !=None and muser !=None): 
			try:
				uauth=db.select('users', where='username=$muser', vars=locals())[0] 
			except:
				return "username does not exist"
			if (mpass==uauth.mpassword and muser==uauth.username): 
		                post = modelblog.get_post(int(id))
               			#form = BlogNew.form()
               			form = BlogSpecial.form()
				form.fill(post)
				return admrender.blogedit(post, form)
			else:
                        	raise web.seeother('/login/blogedit/%s' % id)
                else:
                        raise web.seeother('/login/blogedit/%s' % id)



        def POST(self, id):
                #form = BlogNew.form()
                form = BlogSpecial.form()
                post = modelblog.get_post(int(id))
                if not form.validates():
                        return admrender.blogedit(post, form)
                #modelblog.update_post(int(id), form.d.title, form.d.author, form.d.content,form.d.date)
		db.update('blog', where="id=$id", vars=locals(),
                title=form.d.title, author=form.d.author, content=form.d.content, date=form.d.date, approved=form.d.approved, published=form.d.published)
                raise web.seeother('/blogadmin')
class BlogAdmin: # add login features
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
			if (mpass==uauth.mpassword and muser==uauth.username and uauth.admin=="Yes"): 
				posts = modelblog.get_posts()
				return admrender.blogadmin(posts)
			else:
                        	raise web.seeother('/login/blogadmin')
                else:
                        raise web.seeother('/login/blogadmin')

#############END BLOG#########################################



