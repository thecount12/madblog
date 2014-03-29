import web
import modelblog

urls=(
	"","anything",
	"/blog","Blog",
	'/blogview/(\d+)','BlogView', 
	'/blognew','blogview.BlogNew',
	'/blogdelete/(\d+)','blogview.BlogDelete',
        '/blogedit/(\d+)','blogview.BlogEdit',
        '/blogadmin','blogview.BlogAdmin'

)

render=web.template.render('templates/')
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
                        description="Date:"),
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
			if (mpass==uauth.mpassword and muser==uauth.username): 
				form=self.form() 
				return render.blognew(form)
			else:
                        	raise web.seeother('/login/blognew')
                else:
                        raise web.seeother('/login/blognew')
        def POST(self):
                form = self.form()
                if not form.validates():
                        return render.blognew(form)
                modelblog.new_post(form.d.title, form.d.author, form.d.content, form.d.date)
                raise web.seeother('/blog')

class BlogDelete:
        def POST(self, id):
                modelblog.del_post(int(id))
                raise web.seeother('/blog')
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
               			form = BlogNew.form()
				form.fill(post)
				return render.blogedit(post, form)
			else:
                        	raise web.seeother('/login/blogedit/%s' % id)
                else:
                        raise web.seeother('/login/blogedit/%s' % id)



        def POST(self, id):
                form = BlogNew.form()
                post = modelblog.get_post(int(id))
                if not form.validates():
                        return render.blogedit(post, form)
                modelblog.update_post(int(id), form.d.title, form.d.author, form.d.content,form.d.date)
                raise web.seeother('/blog')
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
			if (mpass==uauth.mpassword and muser==uauth.username): 
				posts = modelblog.get_posts()
				return render.blogadmin(posts)
			else:
                        	raise web.seeother('/login/blogadmin')
                else:
                        raise web.seeother('/login/blogadmin')

#############END BLOG#########################################



