import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import string
from tornado.websocket import WebSocketHandler

def visit(lang,content,inpt):
	fp=open('input','w')
	fp.write(str(inpt))
	fp.close()
	print "Input written"
	print lang
	c = comple()
	if lang == "C":
		content = c.C(content)
	elif lang == "CPP":
		content = c.CPP(content)
	elif lang == "Python":
		content = c.Python(content)
	elif lang == "Java":
		content = c.Java(content)
	elif lang == "Ruby":
		content = c.Ruby(content)

	return content
#	if hasattr("comple()", lang):
#		getattr("comple()", lang)(content)

def errorcomp():
	size = os.path.getsize("err.txt")
	fp = ""
	totalline=""
	print "Stage of Compilin"
	if size <> 0:
		fp=open('err.txt','r')
		readfull = fp.readlines()
		for eachline in readfull:
			totalline = totalline + eachline
			fp.close()
	else :
 		os.system("./a.out > out 2>&1 < input")
		fp=open('out','r')
		readfull = fp.readlines()
		for eachline in readfull:
	 		totalline = totalline + eachline
	 	fp.close()
	return totalline		
		
		
class comple(object):
	def Python(self, content):
		fp=open('temp.py','w')
		fp.write(str(content))
		fp.close()
		os.system("python temp.py 2> err.txt")
		content = errorcomp()
		return content
	def C(self,content):
		print "C  here"
		fp=open('temp.c','w')
		fp.write(str(content))
		fp.close()
		print "Compiling"
		os.system("gcc temp.c 2> err.txt")
		content = errorcomp()
		return content
	def CPP(self,content):
		fp=open('temp.cc','w')
		fp.write(str(content))
		fp.close()
		os.system("g++ temp.cc 2> err.txt")
		content = errorcomp()
		return content
	def Java(self,content):
		fp=open('temp.java','w')
		fp.write(str(content))
		fp.close()
		os.system("javac temp.java 2> err.txt")
		content = errorcomp()
		return content
	def Ruby(self,content):
		fp=open('temp.rb','w')
		fp.write(str(content))
		fp.close()
		os.system("ruby temp.rb 2> err.txt")
		content = errorcomp()
		return content
	
	 				
class Main(tornado.web.RequestHandler):
	def get(self,url=None):
		self.render("login.html")

class Compile(WebSocketHandler):
	def open(self):
		print "New connection opened."

        def on_message(self, message):
        	lang,content,inpt=message.split("//&//")
        	content = u" ".join(content.replace(u"\xa0", u"    ").strip().split())	#for space
        	flag=1
		cont = ""
 		for i in range(len(content)):
 			if content[i]>='0' and content[i]<='9' and flag==1:
 				flag=1
 			else:
 				if content[i]=='>' or content[i]=='{' or content[i]==';':
 					cont =cont + content[i] + '\n'
 				else:
 					cont = cont + content[i]
 				flag=0
        	msg1 = visit(lang,cont,inpt)
        	print msg1
        	self.write_message(cont + "//&//" + msg1);
        	
   	def on_close(self):
                print "Connection closed."
 	
if __name__ == "__main__":
	settings = {
    	"static_path": os.path.join(os.path.dirname(__file__), "static"),
    	}
	application = tornado.web.Application([
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
