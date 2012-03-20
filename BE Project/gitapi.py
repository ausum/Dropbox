
import json;
import os;
def searchrepo():#Complete (Enter any name of repo, searches from all repos on github server)
    
    se="curl http://github.com/api/v2/json/repos/search/" + (raw_input("Enter repository name:")) + " > searchrepo.txt";
    os.system(se);
    f = open("searchrepo.txt");
    d = json.load(f);
    j=0;
    for x in d['repositories']:
	    j=j+1;
    print j
    k=0;
    while (k<j):
	    print "Owner->" + d['repositories'][k]['owner'] + "\tName->" + d['repositories'][k]['name']
	    k+=1;
   
    
def listallrepos():#Complete (Shows the repos of a particular user)
    se="curl http://github.com/api/v2/json/repos/show/" + (raw_input("Enter Username:")) + " > showrepo.txt";
    os.system(se);
    f = open("showrepo.txt");
    d = json.load(f);
    j=0;
    for x in d['repositories']:
	    j=j+1;
    print j
    k=0;
    while (k<j):
	    print "Owner->" + d['repositories'][k]['owner'] + "\tName->" + d['repositories'][k]['name']
	    k+=1;
    
	    
def listallcommits():#Complete
#    se ="curl http://github.com/api/v2/json/commits/list/SolomonPeter26/pyex/master > listcommits.txt"
    se = "curl http://github.com/api/v2/json/commits/list/" + (raw_input("Enter Username:")) + "/" + (raw_input("Enter Repository:")) + "/" + (raw_input("Enter Branch:")) + " > listcommits.txt"
    os.system(se);
    f = open("listcommits.txt");
    d =json.load(f);
    j=0;
    for x in d['commits']:
	    j=j+1;
    print j
    k=0;
    while (k<j):
	    print "Url of commit->" + str(d['commits'][k]['url'])
	    print "Tree ->" + str(d['commits'][k]['tree'])
	    print "Parents ->" + str(d['commits'][k]['parents'])
   	    print "Committed On ->" + str(d['commits'][k]['committed_date'])
   	    print "with message ->" + str(d['commits'][k]['message'])
   	    print "Authored on ->" + str(d['commits'][k]['authored_date'])
	    print "\n\n"
	    k+=1;    
	    
if __name__== "__main__":
    searchrepo()
    listallrepos()
    listallcommits()



#API token required for creating new repo, fork

#    raw_input("\nEnter The choice:-")
#for username in d.values():
#	print username
 
    #for aritcle in d['Sections']['Section'][0]['Article']:
    #  print articles
