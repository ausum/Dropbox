#not needed


import os, glob
import fileinput
import re
def scandirs(path):
        num=0;
        for currentFile in glob.glob( os.path.join(path, '*') ):
            if os.path.isdir(currentFile):
                print '\tgot a directory: ' + currentFile  + "\n"
                scandirs(currentFile)
            print "processing file: " + currentFile
            n=0;
            if re.search("c\Z",currentFile) or  re.search("cpp\Z",currentFile) or re.search("rb\Z",currentFile) or re.search("py\Z",currentFile) or re.search("txt\Z",currentFile):
                for line in fileinput.input(currentFile):
                    n+=1;
                    num+=1;
                print "\t No.of lines: " + currentFile +" has " + str(n) + "\n"

scandirs(raw_input("Enter the path: "))
#print "\n\nTotal Lines of code in folder is:" + str(num) + "\n"
