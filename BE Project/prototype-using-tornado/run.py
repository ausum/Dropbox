import tornado.httpserver
import tornado.ioloop
import tornado.web
import os
import time

aDict = {}
aDict['c']='gcc '
aDict['c++']='gcc '
aDict['python'] = 'python '

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('main.html',code='Enter your code here', output='Your output goes here', filename="Enter Filename",lang="c")


class CompileHandler(tornado.web.RequestHandler):
	def post(self):
		k1=time.time()
		lang1=self.get_argument('lang')
		filename=self.get_argument('filename')
		TypedCode=self.get_argument('code')
		Input=open(filename,'w')
		Input.write(TypedCode)
		Input.close()
		#os.system(aDict[lang1]+filename)
		#os.system("./a.out > "+filename + ".out")
		#Output=open(filename+".out",'r')
		os.system(aDict[lang1]+filename + " 2> "+ filename + ".out")
		str1 = filename + ".out"
		if lang1 == "c" or lang1 == 'c++':
			k=os.path.getsize(str1)
			if k==0 :
				os.system("./a.out ")
		
		k2=time.time()
		str1='\nTime taken :'+ str((k2-k1)*1000) + ' ms'
		self.render('main.html',code=TypedCode,output=str1,filename=filename,lang=lang1)
		
if __name__ == "__main__":
	application = tornado.web.Application([
		(r"/", MainHandler),
		(r"/compile",CompileHandler),
		],
		debug=True)
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(8888)
	tornado.ioloop.IOLoop.instance().start()

