#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import string

def ChangeDashAndSpaceToNothing(MyDir):
    #removes dashes '-' and spaces ' ' in the S01E01 section of filenames to make them easier to work with
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
                print oldname

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
#this whole function probably needs a re-write
    ShowNames = []
    findit = re.compile(r'.S\d{1,2}E\d{1,2}')
    for dirname, dirnames, filenames in os.walk(MyDir,topdown=False):
        for files in filenames:
            foundit = re.search(findit,files.upper())
            if foundit:
                rubbish =  foundit.group()
                x = files.upper().find(rubbish) #x is an integer
                MyShow =  files[:x].title() + rubbish
                if not files[:x].title() in ShowNames:
                    ShowNames.append(MyShow.upper())
                #below captures a dash with single or double spaces around it, or double spaces in general, and periods to change to a single space.
                MyShow = re.sub(r"(\s{1,2}-\s{1,2}|\s\s|(\.))", " ", MyShow,flags=re.I)
                MyShow = re.sub(r"((Marvel?\S{1,2}|Dcs)+?(\s|\.))|(\d{4})", "", MyShow,flags=re.I)
                if "SAMPLE" in MyShow.upper():
                    os.remove(os.path.join(MyDir,MyShow))
                    break
                MyShow = MyShow.replace("S H I E L D","SHIELD")
                MyShow = MyShow + '.mkv'
                try:
                    os.rename(os.path.join(dirname, files),os.path.join(dirname, MyShow))
                except:
                    # maybe need to make a duplicates folder to chuck this in to keep it clean?
                    # or change the name to 'potential duplicate & showname'
                    print 'Potential duplicate: ' + files

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
