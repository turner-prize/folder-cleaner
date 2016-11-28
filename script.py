
import os
import re

#filepath which requires tidying goes below

MyDir = (r'path')
SortFolder(MyDir)

def SortFolder(MyPath):
    UnpackFiles(MyPath)
    CreateShowList(MyPath)
    MoveFiles(MyPath)
            
def find(s, ch):
#function to get the character place of one string within another
    return [i for i, ltr in enumerate(s) if ltr == ch]

def UnpackFiles(MyPath):
#unpacks files from folders, moves anything not a video files to 'other', also deletes .txt and .nfo files
    if not os.path.exists(os.path.join(MyPath,"Other")):
        os.makedirs(os.path.join(MyPath,"Other"))
    Holdr = os.path.join(MyPath,"Other")
    for dirname, dirnames, filenames in os.walk(MyPath,topdown=False):
        for subdir in dirnames:    
            thisfile = os.path.join(dirname, subdir)
            for files in os.listdir(thisfile):
                #moves the videos first, as i was having trouble with if not mkv or not avi....it can;t be both!!
                if files.endswith(".mkv") or files.endswith(".avi") or files.endswith(".mp4"):
                    os.rename (os.path.join(thisfile,files),os.path.join(MyPath,files))
                #deletes .txt files as i was getting a problem with duplicates
                elif files.endswith(".txt") or files.endswith(".nfo") :
                    os.remove (os.path.join(thisfile,files))
                else:
                    #moves the remaining files from their sub directories to the main folder i want them in.
                    os.rename(os.path.join(thisfile, files),os.path.join(Holdr, files))
            #removes empty folders
            if not os.listdir(thisfile):
                os.rmdir(thisfile)
                
def CreateShowList(MyPath):
#finds any instance of e.g. S01E01, S05E15 or whatever within the filename, takes the text before it, and puts it in a list.
#so "Atlanta.S01E01" becomes "Atlanta"
    findit = re.compile(r'.S\d{1,2}E\d{1,2}')
    ShowNames = []
    for dirname, dirnames, filenames in os.walk(MyPath,topdown=False):
        for files in filenames:
            foundit = re.search(findit,files.upper())
            if foundit:
                rubbish =  foundit.group()
                x = files.upper().find(rubbish) #x is an integer
                if not files[:x].title() in ShowNames:
                    ShowNames.append(files[:x].title())
    MakeFolders(ShowNames, MyPath)
    
    
def MakeFolders(ShowList, MyPath):
    for n in ShowList:
        #creates the folders from the list of the shownames, if they dont already exist.
        if not os.path.exists(os.path.join(MyPath,n)):
            os.makedirs(os.path.join(MyPath,n))

def MoveFiles(MyPath):
    #finds any instance of the new folder names within each file, and moves the file to them if there is.
    for dirname, dirnames, filenames in os.walk(MyPath,topdown=False):
        for files in filenames:
            for dirs in dirnames:
                if dirs.upper() in files.upper():
                    print files
                    os.rename(os.path.join(MyPath, files), os.path.join(MyPath, os.path.join(dirs, files)))
