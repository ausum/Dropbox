import os;

def addkey():
    os.chdir('/home/solomon/.ssh')
    print os.listdir(os.getcwd())
    
    #key generate   
    email=raw_input("\n Enter email id: ")
    uname=raw_input("\n Enter github username: ")
    keyg="ssh-keygen -t rsa -f ~/.ssh/" + uname + " -C \"" + email + "\" -P \"\""
    os.system(keyg)
    
    #add ssh key on github
    passwd=raw_input("Enter password : ")
    filen='/home/solomon/.ssh/'+ uname +'.pub'
    f=open(filen,'r')
    rsakey=f.read()
    stradd="curl -u \"" + uname + ":" + passwd + "\" http://github.com/api/v2/json/user/key/add -F \"title=ExeCode\" -F \"key=" + rsakey + "\""
    print "\n" + stradd +"\n"
    os.system(stradd)

#    addssh="ssh-add ~/.ssh/id_rsa_" + email
#    os.system(addssh)


if __name__=="__main__":
    addkey()
