#!/usr/bin/env python
import pexpect,sys,os

filename = "/home/pravin/pexpect/abc.c"
name,ext = filename.split(".")

os.system("cc  " + filename + " -o " + name)

old_stdout=sys.stdout
sys.stdout=open(name + ".out",'w')

p=pexpect.spawn('gdb ' + name)
p.logfile = sys.stdout

while (1==1):
	i=p.expect(['.*[\(gdb\)]',pexpect.EOF])
	if i==0:
		#web socket se input aayega.
		x=raw_input()
		p.sendline(x)
		if x=='q':
			break
		#no.of times
		j=p.expect(['.*[Input :]',pexpect.EOF])
		x=raw_input()
		p.sendline(x)
		j=p.expect(['.*[Input :]',pexpect.EOF])
		x=raw_input()
		p.sendline(x)
		
		
		#yaha hum /def file ko close karenge and contents bhejenge. and then 'a' mode me kholenge
		#Drawback user ko scanf statement k pehle Input: aisa likhna padhega ya hume karna padega
		
	elif i==1:
		break

sys.stdout=old_stdout
fp=open(name + ".out",'r')
b=fp.readlines()
for e in b:
	print e,
fp.close()

