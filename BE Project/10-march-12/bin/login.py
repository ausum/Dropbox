import tornado.web
import getpass
import tornado.httpserver
import tornado.ioloop
import string
import MySQLdb as mdb

class User(tornado.web.RequestHandler):
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
		
		if op=="login":
			uname=self.get_argument('uname')
			pwd=self.get_argument('pwd')
			cur.execute("SELECT pwd FROM user where uname=%s",uname)
			numrows = int(cur.rowcount)
			if numrows==0 :
				print "not registered"
			else:
				row = cur.fetchone()
				if pwd==row[0]:
					#get the repo's here
					try:
						os.makedirs("/home/"+getpass.getuser()+"/"+uname)
						os.makedirs("/home/"+getpass.getuser()+"/"+uname+"/Private")
						os.makedirs("/home/"+getpass.getuser()+"/"+uname+"/Circle")
					except:
						print "already exists"
					os.system("./repoDown "+uname)
					self.write("welcome to ExeCode")
		else:
			print op
			mail=self.get_argument('rEmail')
			print mail
			#git auth cmd > git.txt
			os.system("./uname git.txt > uname.txt")
			fp=open("uname.txt","r")
			uname=fp.readline()
			fp.close()
			if uname==self.get_argument('username'):
				print "registered"

