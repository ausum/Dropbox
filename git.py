import os
import json

def createrepo():
            #change directory
    folpath=""
    fold=raw_input("Enter repository name ");
    uname=raw_input("Enter User name ");
    chp="/home/solomon/" + uname + "/Private"
    os.chdir(chp)
    folpath=" mkdir " + str(fold)
    os.system(folpath)
    chp="/home/solomon/" + uname + "/Private/" + fold
    os.chdir(chp)
    os.system(" touch README.md");
    print "\n"
    print os.listdir(os.getcwd())
    initgit(fold,uname)
    
def createmaindir():
    uname=raw_input("Enter User name ");
    chp="/home/solomon/"
    os.chdir(chp)
    folpath=" mkdir " + str(uname)
    os.system(folpath)
    chp="/home/solomon/" + uname
    os.chdir(chp)
    os.system("mkdir Private")
        
    
def pushgithub():    #commits on local repo and pushes to remote repo
    fold=raw_input("Enter repository name ");
    uname=raw_input("Enter User name ");
    chp="/home/solomon/" + uname + "/Private/" + fold
    os.chdir(chp)
    print "\n\n"
    print os.listdir(os.getcwd())   #shifted to local repo
    os.system("git remote")
    bran=raw_input("Enter remote branch ");     #select which remote branch you want to go to
    commitlocal()                   #commits on local repo
    remotepush(bran,uname,fold)     #pushes to remote repo
    

     
def initgit(fold,uname):
            # only INITIALISE GIT IN FOLDER
    se="curl http://github.com/api/v2/json/user/show/" + (raw_input("Enter user name:")) + " > username.txt";
    print se
    os.system(se);
    f = open("username.txt");
    d = json.load(f);
    un = "git config --global user.name \"" + str(d['user']['name']) + "\"" 
    em=  "git config --global user.email \"" + str(d['user']['email']) +"\""
    os.system(un)
    os.system(em)
    os.system(" git init")
    commitlocal()
    remotel(fold)
    os.system("git remote")
    bran=raw_input("Enter remote branch ");     #select which remote branch you want to go to
    remotepush2(bran,uname,fold)
    
def commitlocal():
            #add files for commit
    os.system(" git add .")
    stri=" git commit -m \" " + (raw_input("Enter message for commit:")) + "\""
    
            #view log of commits
    print "\t\tLocal ->"
    os.system(stri)
    os.system(" git log")
    
            #view status of repository
    print "\t\tStatus ->"
    os.system(" git status")
    
            #view files which have been commited
    print "\t\tCommited Files ->"
    os.system(" git ls-files")
    
def remotel(fold):    
    print "\t\tRemote ->"
    os.system(" git remote")


    tok=raw_input("Enter Github API token ");
    crn="curl -F 'login=SolomonPeter26' -F 'token=" + tok + "' https://github.com/api/v2/json/repos/create -F 'name=" + fold + "' -F 'description=" + raw_input("Enter description for project: ") + "\'"
    print crn
    os.system(crn)

#function to push on github  
def remotepush(bran,uname,fold):
#    strr=" git remote add " + brname + " git@github.com:" + uname + "/" + fold + ".git"
#    print strr
#    os.system(strr)
    strr2="git push " + bran + " master"
    print strr2
    os.system(strr2)
    
def remotepush2(bran,uname,fold):
    strr=" git remote add " + bran + " git@peterkingsley26@gmail.com:" + uname + "/" + fold + ".git"
    print strr
    os.system(strr)
    strr2="git push " + bran + " master"
    print strr2
    os.system(strr2)

if __name__ == "__main__" :
   #ch=str(raw_input("Enter choice:"))
   #if ch=='1':
       createrepo()
   #elif ch=='2':
       pushgithub()
#   elif ch==3:
 #      createmaindir()
