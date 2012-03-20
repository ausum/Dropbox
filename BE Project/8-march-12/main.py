#!/usr/bin/env python

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler
import MySQLdb as mdb
import os, re ,fileinput
from datetime import date

class Main(WebSocketHandler):
	def get(self):
		self.render("login.html");

#handling file options
class File(WebSocketHandler):
	def open(self):
		try:
			global con
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		print "Connection for file handling"
		
	def on_message(self,message):
		print message
		option, user, project,Type, param=message.split("$&")
		
		if(option=="open"):
			print "opening file"
			fp=open(param,"r")
			lines=fp.readlines()
			line=""
			for l in lines:
				line=line+l
			self.write_message("open$&"+line);
			fp.close()
			
		elif option=="create":
			command="cat > "+"/home/"+os.getlogin()+"/"+user+"/"+Type+"/"+project+"/"+param
			print command
			os.system(command)
			self.write_message("File creating")
			
		elif option=="save":
			print "save"
			filename,content=param.split("/~/")
			fp=open(filename,"w")
			fp.write(content)
			fp.close()
		elif option=="compile":
			filename=param
			ext=filename[-2:]
			if ext==".c" or ext=="pp":
				command="gcc "+filename+" -o "+ filename+".out 2>" + filename+".err"
			elif ext=="py":
				command="python "+filename+" -o "+ filename+".out 2>" + filename+".err"
			elif ext=="rb":
				command="ruby "+filename+" 2>" + filename+".err"
			elif ext=="va":
				command="javac "+filename+" 2>" + filename+".err"
			
			print command
			os.system(command)
			fp=open(filename+".err","r")
			lines=fp.readlines()
			line=""
			for l in lines:
				line=line+l
			
			print line
			fp.close()
			self.write_message("errors$&"+line);
			
		elif option=="execute":
			filename,Input=param.split("/~/")
			print filename,Input
			ext=filename[-2:]
			fp=open(filename+".in",'w')
 			fp.write(str(Input))
 			fp.close()
			if ext==".c" or ext=="pp":
				command=""+filename+".out >"+ filename+".output 2>&1 <" + filename+".in"
			elif ext=="py":
				command=""+filename+".out >"+ filename+".output 2>&1 <" + filename+".in"
			elif ext=="rb":
				command="ruby "+filename+" 2>" + filename+".err"
			elif ext=="va":
				command="java "+filename+" 2>" + filename+".err" #check this
			
 			totalline=""
			os.system(command)
			fp=open(filename+".output",'r')
			readfull = fp.readlines()
			for eachline in readfull:
 				totalline = totalline + eachline
 			print totalline
			fp.close()
				
			self.write_message("output$&"+totalline)
			
	def on_close(self):
		print "file connection closed"

#handling user options
class User(WebSocketHandler):
        def open(self):
            print "New connection opened."

        def on_message(self, message):
			uname,email,pwd=message.split(",")
			
			#get registration info
			os.system("curl -i http://github.com/api/v2/xml/user/email/"+email+" > tempAcc.txt")
			os.system("./uname tempAcc.txt > tmpAcc.txt")
			fp=open("tmpAcc.txt","r")
			
			Actual=str(fp.readline())
			fp.close()
			#check validity
			if uname==str(Actual):
				try:
					global con
					con = mdb.connect('localhost', 'root','amarok18', 'testdb');
					global cur
					cur = con.cursor()

				except mdb.Error, e:
					print "Error %d: %s" % (e.args[0],e.args[1])
					sys.exit(1)
				#insert into database
				try:
					query="insert into user values('"+uname+"','"+email+"','"+pwd+"')"
					cur.execute(query)
				except:
					self.write_message("Account Already Exists..")
				
				#check insertion status
				self.write_message("Registered")
			else:
				self.write_message("Some Error Occured...")

        def on_close(self):
                print "Connection closed."




def calculateKLOC(current):
	num=0;
	for top, dirs, files in os.walk(current):
		for nm in files:       
		    currentFile = os.path.join(top, nm)

		    n=0;
		    if re.search("c\Z",currentFile) or  re.search("cpp\Z",currentFile) or re.search("rb\Z",currentFile) or re.search("py\Z",currentFile) or re.search("java\Z",currentFile):
	   		        
		            for line in fileinput.input(currentFile):
		                n+=1;
		                num+=1;
		            print currentFile
		            print "\t No.of lines: " + currentFile +" has " + str(n) + "\n"
		        
	print "\n\nTotal Lines of code in folder is:" + str(num) + "\n"
	
	return str(num)
	
#handling project options
class Project(WebSocketHandler):
	def open(self):
		try:
			global con
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
		
		print "Project creation"
	
	def on_message(self,message):
		option,user,name, param=message.split(",")
		print option, user, name, param
		if(option=="create"): 
		#create new project
			desc, Type,members =param.split("$")
			print desc, Type
			
		
			if Type=="Circle":
				id1,id2,id3=members.split("&") #limited members ====> change here
				print id1, id2
				today=str(date.today())
				try: #decide if public project's entry is to be saved in db or not
					query="insert into invitations values('"+user+"','"+name+"','"+id1+"','"+today+"','Pending')"
					cur.execute(query)
					query="insert into invitations values('"+user+"','"+name+"','"+id2+"','"+today+"','Pending')"
					cur.execute(query)
				except mdb.Error, e:
					self.write_message("Error in creation"+e.args[0])
			
			try: #decide if public project's entry is to be saved in db or not
				query="insert into project values('"+name+"','"+desc+"','"+user+"')"
				cur.execute(query)
			except mdb.Error, e:
				self.write_message("Error in creation"+str(e.args[0]))
			
			if Type!="Public":
				os.mkdir("/home/"+os.getlogin()+"/"+user+"/"+Type+"/"+name)
			else:
				print "making public repo"
				os.mkdir("/home/"+os.getlogin()+"/"+Type+"/"+name)
			
			self.write_message("Project Created")
		elif(option=="update"):	#update project
			if(param=="GET"):
				query="select descr from project where name='"+name+"';"
				cur.execute(query)
				total=int(cur.rowcount)
				print total
				if(total==1):
					row=cur.fetchone()
					query="select * from invitations where sender='"+user+"' and project='"+name+"';"
					cur.execute(query)
					if(cur.rowcount):
						Type="circle"
					else:
						Type="private"
					self.write_message("update,SET,"+row[0]+","+Type)
				else: #if user is not owner of the project
					self.write_message("update,ERROR, ")
			else:
				#param="SET"..updating database
				pass
			print "update project"
		elif(option=="cocomo"):	# find the cocomo estimates
			#calculate the project estimate by passing the username and project name avail in user and name resp
			#find KLOC first
			path="/home/"+os.getlogin()+"/"+user+"/Circle/"+name
			print path
			KLOC=4 #float(calculateKLOC(path))
			ab=3.0
			bb=1.12
			cb=2.5
			db=0.35
			efforts=ab*pow(KLOC,bb)
			devTime=cb*pow(efforts,db)
			persons=int(efforts/devTime)
			message="cocomo,<b><h2> Estimates for Project : </b>"+name +"</h2>"+\
				"<table>"+\
				"<tr><td><b> Efforts in Person-Month : </b></td><td>"+str(efforts)+" Month/s </td></tr><br>" + \
				"<tr><td><b> Development Time (in Months) :</b></td><td>"+str(devTime)+"</td></tr><br> "+\
				"<tr><td><b> Persons Required : </b></td><td>"+str(persons)+"</td></tr><br><br>"+\
				"<tr align='center'><td><input type='button' value='Ok' class='buttonCancel'/><td></tr></table>"
					
			self.write_message(message)
					
		elif(option=="respondInvite"):
			print user +" "+ param + "ed invitation for " +name
			query="update invitations set status='"+param+"ed' where receiver in (select email from user where user='"+user+"') and project='"+name+"';"
			cur.execute(query);
			self.write_message(param);
		else:
			#save changes
			print "save changes here"
	

#handling tree view
class TreeView(WebSocketHandler):
	def open(self):
		print "Request for tree view"
		
	def on_message(self,message):
		Folders=[]
		Files=[]
		path=[]
		ulist=[]
		print message
		ulist.append(message)	#message is the username
		route="/home/"+os.getlogin()+"/"+ulist[0]
		path.append(route)
		for dirname, dirnames, filenames in os.walk(path[0]):
		    for subdirname in dirnames:
		        Folders.append(os.path.join(dirname, subdirname))
		    for filename in filenames:
		    	ext = os.path.splitext(filename)[-1][1:]
		    	Files.append(os.path.join(dirname, filename))
		self.write_message("This is the response : "+message)
#		self.write_message(Folders,Files,path)
		

#showing invitations
class Invitations(WebSocketHandler):
	def open(self):
		print "Showing invitations"
		try:
			global con
			con = mdb.connect('localhost', 'root','amarok18', 'testdb');
			global cur
			cur = con.cursor()

		except mdb.Error, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			sys.exit(1)
	
	def on_message(self,message):
		print message
		row=[]
		query="select count(*) from invitations where receiver = (select email from user where user='"+message+"');"
		print query
		cur.execute(query)
		row = cur.fetchone()
		
		total=row[0]
		#self.write_message(total+" invitations")
		#self.write_message(str(row[0]))
		#query="select sender, project, senton,status from invitations where receiver = (select email from user where user='"+message+"');"
		query="select i.sender,i.project,p.descr,i.senton,i.status from invitations i, project p where p.name=i.project and receiver in (select email from user where user='"+message+"');"

		cur.execute(query)
		i=1
		if(total>0):
			row=cur.fetchone()
			message=str(total)+"$"+row[0]+" invited you for \
			<br> <b> Project: </b>"+ row[1]+\
			"<br> <b>Project Description  : </b>"+row[2]+\
			"<br><b>On</b>:" + row[3]+" <b>Status</b> : <span id='span"+row[1]+"'>"+row[4]+"</span><br>\
			<input type='button' value='Accept' id='"+row[1]+"' onclick='javascript:acceptInvite(this.id)' />" +\
			"<input type='button' value='Reject' id='"+row[1]+"' onclick='javascript:rejectInvite(this.id)' /><br>"
			print message
			while i< total:
				row=cur.fetchone()
				message=message+"&"+row[0]+" invited you for \
				<br><b> Project </b>: "+row[1]+\
				"<br><b>Project Description : </b>  "+row[2]+ \
				"<br><b>On: </b>"+ row[3]+"  <b>Status : </b>""<span id='span"+row[1]+"'>"+row[4]+"</span><br>\
				<input type='button' value='Accept' id='"+str(row[1])+"' onclick='javascript:acceptInvite(this.id)' />"+\
				"<input type='button' value='Reject' id='"+row[1]+"' onclick='javascript:rejectInvite(this.id)' /><br>"
				i=i+1
				print message
				
		self.write_message(str(message))		
		
print "Web socket server started."
HTTPServer(Application([(r"/register", User),(r"/file",File),(r"/project",Project),(r"/tree",TreeView),(r"/invitations",Invitations)],debug=True)).listen(7777)
IOLoop.instance().start()
