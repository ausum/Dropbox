#!/usr/bin/env python
import pexpect,sys,os

filename = "/home/pritam/Pravin-Nagare/Private/try/abc.c"

name,ext = filename.split(".")
#.*	fprintf(fp,"%s",yytext);
#[scanf\(\".*\"\)\;] {fprintf(fp,"printf(\"Input :\");); fprintf(fp,\"%s\",yytext)}

os.system("cc " + filename + " -o " + name)

old_stdout=sys.stdout
sys.stdout=open(name + ".out",'w')

p=pexpect.spawn(name)
p.logfile = sys.stdout

while (1==1):
	i=p.expect(['.*[Input:]',pexpect.EOF])
	if i==0:
		#/filename.out k contents web socket se bhejna ha output window ko.
		#web socket se input aayega. instead of raw_input
		x=raw_input()
		p.sendline(x)
		#yaha hum /filename.out file ko close karenge and contents bhejenge.
		#Drawback user ko scanf statement k pehle Input: aisa likhna padhega ya hume karna padega
		
	elif i==1:
		break

sys.stdout=old_stdout
fp=open(name + ".out",'r')
b=fp.readlines()
for e in b:
	print e,
fp.close()

