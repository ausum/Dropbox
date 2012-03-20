import os;

def createmaindir():
    uname=raw_input("Enter User name ");
    chp="/home/solomon/"
    os.chdir(chp)
    folpath=" mkdir " + str(uname)
    os.system(folpath)
    chp="/home/solomon/" + uname
    os.chdir(chp)
    os.system("mkdir Private")
    
def createssh():
    email=raw_input("Enter email id");
    keygen="ssh-keygen -t rsa -C \"" + email + "\""
    
if __name__ == "__main__" :
    createmaindir()
    
