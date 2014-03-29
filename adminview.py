import web

urls=(
        "","anything",
        "/admin","Admin"

)

render=web.template.render('templates/')
db=web.database(dbn='sqlite',db='multi.db')


class anything: #important path back to code.py or root
        def GET(self): raise web.seeother('/')

##########BEGIN ADMIN SECTION################

class Admin: # just a private page example that requires login
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
                                return render.admin() # test redirect
                        else:
                                raise web.seeother('/login/admin')
                else:
                        raise web.seeother('/login/admin')


