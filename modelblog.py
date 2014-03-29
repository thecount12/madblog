import os, sys 
import web 
#abspath = os.path.dirname(__file__)
#sys.path.append(abspath)
#os.chdir(abspath)


db=web.database(dbn='sqlite',db='multi.db')

def get_posts():
	return db.select('blog', order='id DESC')

def get_post(id):
	try:
		return db.select('blog', where='id=$id', vars=locals())[0]
	except IndexError:
		return None

#def new_post(title, author, username, text ,date):
def new_post(title, author, text ,date):
	db.insert('blog', title=title, author=author, content=text, date=date)

def del_post(id):
	db.delete('blog', where="id=$id", vars=locals())

def update_post(id, title, author, text, date ):
	db.update('blog', where="id=$id", vars=locals(),
		title=title, author=author, content=text, date=date)

if __name__=="__main__":
	pass
	new_post("mtitle","William Gunnells","coool stuff","3/24/2012")
	#del_post(1) 
