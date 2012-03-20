import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import string
from tornado.websocket import WebSocketHandler

url1 = ""

class Main(tornado.web.RequestHandler):
	def get(self,url=None):
		Folders=[]
		Files=[]
		path=[]
		op=0
		
		print str(url)
		global url1
		url1 = str(url)
		print op
		path.append(os.getcwd())
		for dirname, dirnames, filenames in os.walk(path[0]):
		    for subdirname in dirnames:
		        Folders.append(os.path.join(dirname, subdirname))
		    for filename in filenames:
		    	ext = os.path.splitext(filename)[-1][1:]
		    	if ext == 'c' or ext == 'cpp' or ext == 'java' or ext == 'py' or ext == 'rb':
			        Files.append(os.path.join(dirname, filename))
	
		
		if str(url) == "None":
			self.render('home.html',dirList=Folders,fileList=Files,fpath=path,textarea="",inpu="",ou="")
   		else:
   			u = '/'+url
   			a = open(u,"r")
   			b = a.readlines()
   			a.close()
   			self.render('home.html',dirList=Folders,fileList=Files,fpath=path,textarea=b,inpu="",ou="")
 		
class Compile(WebSocketHandler):
	def open(self):
            print "New connection opened."

        def on_message(self, message):
        	option,content=message.split("/&/")
 		
 		if option == "compile":
	 		totalline= ""
 			fp=open('input','w')
 			fp.write(str(content))
 			fp.close()
 		
 			global url1
 			u = '/'+url1
 			os.system("gcc "+u+" 2> err.txt")
 			size = os.path.getsize("err.txt")
 			if size <> 0:
 				fp=open('err.txt','r')
 				readfull = fp.readlines()
 				for eachline in readfull:
		 			totalline = totalline + eachline
 				fp.close()
 				print totalline
 				
			else :
 				os.system("./a.out > out 2>&1 < input")
				fp=open('out','r')
				readfull = fp.readlines()
				for eachline in readfull:
	 				totalline = totalline + eachline
	 			print totalline
				fp.close()
				
			self.write_message(totalline)
 		elif option == "save":
 			#content = content.encode("utf-8")
 			#content = u" ".join(content.replace(u"\xa0", u" ").strip().split())	#for space
 			fp = open("/" + url1,"w")
 			flag=1
 			for i in range(len(content)):
 				#if content[i]>=' ' and flag==1:
 				#	flag=1
 				#else:
 				fp.write(content[i])
 				#	flag=0
 			fp.close()
 			
 			self.write_message(content)
   	def on_close(self):
                print "Connection closed."
 	

if __name__ == "__main__":
	settings = {
    	"static_path": os.path.join(os.path.dirname(__file__), "static"),
    	}
	application = tornado.web.Application([
		(r"/([a-z\?]*[a-zA-Z0-9\/]*[a-zA-Z]*[\.][a-z]*)",Main),
		(r"/",Main),
		],debug=True,
		**settings)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	application1 = tornado.web.Application([
		(r"/compile",Compile),
		],debug=True,
		**settings)
	http_server1 = tornado.httpserver.HTTPServer(application1)
	http_server1.listen(7777)
	tornado.ioloop.IOLoop.instance().start()
