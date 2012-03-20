import tornado.httpserver
import tornado.ioloop
import tornado.web
import getpass
import tornado.httpserver
import tornado.ioloop
import string
import MySQLdb as mdb
import os

class Login(tornado.web.RequestHandler):
	con = None
	cur=None
	
	def post(self,op):
		try:
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)

		uname=self.get_argument('uname')
		pwd=self.get_argument('pwd')
		query="SELECT pwd FROM user where user='"+uname+"'"
		cur.execute(query)
		numrows = int(cur.rowcount)
		if numrows==0 :
			self.write("<html><body><h3>Not registered :-( </h3></body></html>")
		else:
			row = cur.fetchone()
			if pwd==row[0]:
				me=os.getlogin()
				#get the repo's here
				try:

					os.makedirs("/home/"+me+"/"+uname)
					os.makedirs("/home/"+me+"/"+uname+"/Private")
					os.makedirs("/home/"+me+"/"+uname+"/Circle")
				except:
					print "NO need to create folders"
				os.system("./repoDown "+uname+" "+me)



class Main(tornado.web.RequestHandler):
	def get(self):
		self.render("login.html");
		

if __name__ == "__main__":
	settings = {
    	"static_path": os.path.join(os.path.dirname(__file__), "static"),
    	}
	application = tornado.web.Application([
		(r"/",Main),
		(r"/(login)",Login),
		],debug=True,
		**settings)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
