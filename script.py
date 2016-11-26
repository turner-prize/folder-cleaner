import os

MyDir = "C:\Users\Turner_prize\Desktop\Python Test"

#function to get the character place of one string within another
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

findit = re.compile(r'.S\d\dE\d\d')
ShowNames = []

#deletes any .txt or .jpg files which are sometimes found in torrent folders.
for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
    for subdir in dirnames:    
        thisfile = os.path.join(dirname, subdir)
        for files in os.listdir(thisfile):
            if files.endswith(".txt") or files.endswith(".jpg"): 
                os.remove(os.path.join(thisfile, files))
            else:
                #moves the remaining files from their sub directories to the main folder i want them in.
                os.rename (os.path.join(thisfile,files),os.path.join(MyDir,files))
    #deletes all the now empty folders.
    for dname in dirnames:
        dFile = os.path.join(dirname,dname)
        if not os.listdir(dFile):
            os.rmdir(dFile)
            
#finds any instance of e.g. S01E01, S05E15 or whatever within the filename, takes the text before it, and puts it in a list.
#so "Atlanta.S01E01" becomes "Atlanta"
for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
    for files in filenames:
        foundit = findit.search(files.upper())
        rubbish =  foundit.group()
        x = files.upper().find(rubbish) #x is an integer
        if not files[:x].title() in ShowNames:
            ShowNames.append(files[:x].title())

for n in ShowNames:
    #creates the folders from the list of the shownames, if they dont already exist.
    if not os.path.exists(os.path.join(MyDir,n)):
        os.makedirs(os.path.join(MyDir,n))
        
#finds any instance of the new folder names within each file, and moves the file to them if there is.
for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
    for files in filenames:
        for dirs in dirnames:
            if dirs.upper() in files.upper():
                os.rename(os.path.join(MyDir, files), os.path.join(MyDir, os.path.join(dirs, files)))
        
