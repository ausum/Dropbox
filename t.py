import os , re ,fileinput
num=0;
for top, dirs, files in os.walk(raw_input("Enter the path: ")):
    for nm in files:       
        currentFile = os.path.join(top, nm)
        print currentFile
        n=0;
        if re.search("c\Z",currentFile) or  re.search("cpp\Z",currentFile) or re.search("rb\Z",currentFile) or re.search("py\Z",currentFile) or re.search("txt\Z",currentFile):
                for line in fileinput.input(currentFile):
                    n+=1;
                    num+=1;
                print "\t No.of lines: " + currentFile +" has " + str(n) + "\n"
            
print "\n\nTotal Lines of code in folder is:" + str(num) + "\n"
