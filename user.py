import json;
import os;
def userinfo():#Complete (Enter any name of repo, searches from all repos on github server)
    se="curl http://github.com/api/v2/json/user/show/" + (raw_input("Enter user name:")) + " > username.txt";
    print se
    os.system(se);
    f = open("username.txt");
    d = json.load(f);
#    print d
    print d['user']['name']
    print d['user']['email']
    
if __name__ == "__main__" :
    userinfo()
