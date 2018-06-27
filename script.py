#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import string

def ChangeDashAndSpaceToNothing(MyDir):
    findit = re.compile(r'S\d{1,2}.E\d{1,2}')
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
            for files in filenames:
                x = findit.findall(files)
                if x:
                    y = re.sub(r"\s|-", "", x[0])
                    y = string.replace(files,x[0],y)
                    oldname = "%s/%s" % (dirname,files)
                    newname = "%s/%s" % (dirname,y)
                    os.rename(oldname,newname)

def CreateSeasonFolders(MyDir):
    findit = re.compile(r'S\d{1,2}')
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
            for files in filenames:
                x = findit.findall(files)
                if x:
                    MySeason = re.sub(r"S0|S", "", x[0])
                    FolderName = "Season %d" % int(MySeason)
                    NewPath = "%s/%s" % (dirname,FolderName)
                    if not os.path.isdir(NewPath):
                        os.mkdir(NewPath)
                    OldFullPath = "%s/%s" % (dirname,files)
                    NewFullPath = "%s/%s" % (NewPath,files)
                    os.rename(OldFullPath,NewFullPath)

def UnpackFiles(MyDir):
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        for files in filenames:
            oldname = "%s/%s" % (dirname,files)
            newname = "%s/%s" % (MyDir,files)
            if os.path.getsize(oldname) >100:
		os.rename(oldname,newname)
		
def DeleteLittleFiles(MyDir):
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        for files in filenames:
            oldname = "%s/%s" % (dirname,files)
            if os.path.getsize(oldname) <500000:
                os.remove(oldname)

def DeleteEmptyFolders(MyDir):
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        if len(dirnames) == 0:
            os.rmdir(dirname)

def MakeFolders(ShowList, MyPath):
    for n in ShowList:
        #creates the folders from the list of the shownames, if they dont already exist.
        if not os.path.exists(os.path.join(MyPath,n)):
            os.makedirs(os.path.join(MyPath,n))

def CreateShowList(MyDir):
#finds any instance of e.g. S01E01, S05E15 or whatever within the filename, takes the text before it, and puts it in a list.
#so "Atlanta.S01E01" becomes "Atlanta"
    findit = re.compile(r'.S\d{1,2}E\d{1,2}')
    ShowNames = []
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        for files in filenames:
            foundit = re.search(findit,files.upper())
            if foundit:
                rubbish =  foundit.group()
                x = files.upper().find(rubbish) #x is an integer
                if not files[:x].title() in ShowNames:
                    ShowNames.append(files[:x].title())
    MakeFolders(ShowNames, MyDir)

def ChangeShowNames(MyDir):
#checks folder for TV Shows, adds them to list to compare later.
    ShowNames = []
    findit = re.compile(r'.S\d{1,2}E\d{1,2}')
    sYear = re.compile(r'\d{4}\s')
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        for files in filenames:
            foundit = re.search(findit,files.upper())
            if foundit:
                rubbish =  foundit.group()
                x = files.upper().find(rubbish) #x is an integer
                MyShow =  files[:x].title() + rubbish
                MyShow = MyShow.replace("."," ")
                foundYear = re.search(sYear,MyShow)
                if foundYear:
                    MyShow = re.sub(r'\d{4}\s',"",MyShow)
                if not files[:x].title() in ShowNames:
                    ShowNames.append(MyShow.upper())
                if "Dcs" in MyShow:
                    MyShow = MyShow.replace("Dcs ","")
                if "Marvel" or "Marvels" in MyShow:
                    MyShow = re.sub(r"Marvel\s|Marvels\s", "", MyShow)
                if " - " in MyShow:
                    MyShow = MyShow.replace(" - "," ")
                if "SAMPLE" in MyShow.upper():
                    os.remove(os.path.join(MyDir,MyShow))
                    break
                if "S H I E L D"in MyShow:
                    MyShow = MyShow.replace("S H I E L D","SHIELD")
                MyShow = MyShow + '.mkv'
		MyShow = re.sub("  "," ",MyShow)
                try:
                    os.rename(os.path.join(dirname, files),os.path.join(dirname, MyShow))
                except:
                    print 'error! changeshownames'
                    print files

def MoveFiles(MyDir):
    #finds any instance of the new folder names within each file, and moves the file to them if there is.
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        for files in filenames:
            for dirs in dirnames:
                if dirs.upper() in files.upper():
                    try:
                        os.rename(os.path.join(MyDir, files), os.path.join(MyDir, os.path.join(dirs, files)))
                    except:
                        print 'error! movefiles'
                        print files

def RemoveEmpties(MyDir):
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        if not os.listdir(dirname):
            os.rmdir(dirname)

def music(fPath):
    try:
        tag = TinyTag.get(fPath)
        if tag:
            filename, file_extension = os.path.splitext(fPath)
            if file_extension != '.mp4':
                print fPath
                return True
    except:
        return False

def MoveToMusic(OldPath,filename):
    MusicPath = os.path.join(r'/mnt/usb/Dan/Music',filename)
    os.rename(OldPath,MusicPath)


def DoTheLot():
	MyDir = (r'D:\Dan\TV')
	DeleteLittleFiles(MyDir)
	UnpackFiles(MyDir)
	RemoveEmpties(MyDir)
	ChangeDashAndSpaceToNothing(MyDir)
	ChangeShowNames(MyDir)
	CreateShowList(MyDir)
	MoveFiles(MyDir)
	CreateSeasonFolders(MyDir)

if __name__ == "__main__":
    DoTheLot()
