#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import string

def ChangeDashAndSpaceToNothing(MyDir):
    #removes dashes '-' and spaces ' ' in the S01E01 section of filenames to make them easier to work with
    findit = re.compile(r'S\d{1,2}.E\d{1,2}')
    for files in os.listdir(MyDir):
            x = findit.findall(files)
            if x:
                y = re.sub(r"\s|-", "", x[0])
                oldname = "%s/%s" % (MyDir,files)
                newname = "%s/%s" % (MyDir,files.replace(x[0],y))
                os.rename(oldname,newname)

def UnpackFiles(MyDir):
    MainDir = (os.path.join(os.getcwd(),'test-folder'))
    for i in os.listdir(MyDir):
        if os.path.isdir(os.path.join(MyDir,i)):
            UnpackFiles(os.path.join(MyDir,i))
        else:
            oldname = os.path.join(MyDir,i)
            newname = os.path.join(MainDir,os.path.basename(oldname))
            os.rename(oldname,newname)
	
def DeleteLittleFiles(MyDir):
    for i in os.listdir(MyDir):
        if os.path.isdir(os.path.join(MyDir,i)):
            DeleteLittleFiles(os.path.join(MyDir,i))
        else:
            oldname = os.path.join(MyDir,i)
            if os.path.getsize(oldname) <500000:
                os.remove(oldname)

def DeleteEmptyFolders(MyDir):
    for i in os.listdir(MyDir):
        if os.isdir(os.path.join(MyDir,i)):
            print(i)

def CreateShowFolders(MyDir):
#finds any instance of e.g. S01E01, S05E15 or whatever within the filename, takes the text before it, and puts it in a list.
#so "Atlanta.S01E01" becomes "Atlanta"
    findit = re.compile(r'.S\d{1,2}E\d{1,2}')
    for files in os.listdir(MyDir):
        foundit = re.search(findit,files.upper()).group()
        if foundit:
            x = files.upper().find(foundit) #x is an integer
            MyShow = os.path.join(MyDir,files[:x].title())
            if not os.path.exists(MyShow):
                os.makedirs(MyShow)
            season = re.compile(r'S\d{1,2}')
            y = season.findall(files)
            if y:
                MySeason = re.sub(r"S0|S", "", y[0])
                FolderName = "Season %d" % int(MySeason)
                NewPath = "%s/%s" % (MyShow,FolderName)
                if not os.path.isdir(NewPath):
                    os.mkdir(NewPath)


def ChangeShowNames(MyDir):
#checks folder for TV Shows, adds them to list to compare later.
#this whole function probably needs a re-write
    findit = re.compile(r'.S\d{1,2}E\d{1,2}')
    for files in os.listdir(MyDir):
        foundit = re.search(findit,files.upper())
        if foundit:
            SxxExx =  foundit.group()
            x = files.upper().find(SxxExx) #x is an integer
            MyShow =  files[:x].title() + SxxExx
            if files[:x] in files:
                #below captures a dash with single or double spaces around it, or double spaces in general, and periods to change to a single space.
                MyShow = re.sub(r"(\s{1,2}-\s{1,2}|\s\s|(\.))", " ", MyShow,flags=re.I)
                MyShow = re.sub(r"((Marvel?\S{1,2}|Dcs)+?(\s|\.))|(\d{4})", "", MyShow,flags=re.I)
                if "SAMPLE" in MyShow.upper():
                    os.remove(os.path.join(MyDir,MyShow))
                    break
                MyShow = MyShow.replace("S H I E L D","SHIELD")
                MyShow = MyShow + '.mkv'
                try:
                    os.rename(os.path.join(MyDir, files),os.path.join(MyDir, MyShow))
                except:
                    # maybe need to make a duplicates folder to chuck this in to keep it clean?
                    # or change the name to 'potential duplicate & showname'
                    print ('Potential duplicate: ' + files)

def MoveFiles(MyDir):
    #finds any instance of the new folder names within each file, and moves the file to them if there is.
    for files in os.listdir(MyDir):
        if not os.path.isdir(os.path.join(MyDir,files)):
            findit = re.compile(r'.S\d{1,2}E\d{1,2}')
            foundit = re.search(findit,files.upper()).group()
            x = files.upper().find(foundit) #x is an integer
            ShowName = files[:x].title()
            ShowPath = os.path.join(MyDir,ShowName)
            y = re.compile(r'S\d{1,2}')
            y = y.findall(files)
            MySeason = re.sub(r"S0|S", "", y[0])
            SeasonPath = os.path.join(ShowPath,"Season %d" % int(MySeason))
            OldName = os.path.join(MyDir,files)
            NewName = os.path.join(SeasonPath,files)
            os.rename(OldName,NewName) 

def RemoveEmpties(MyDir):
    for i in os.listdir(MyDir):
        if os.path.isdir(os.path.join(MyDir,i)):
            if not (os.listdir(os.path.join(MyDir,i))):
                os.rmdir(os.path.join(MyDir,i))


def DoTheLot():
	MyDir = (os.path.join(os.getcwd(),'test-folder'))
	DeleteLittleFiles(MyDir)
	UnpackFiles(MyDir)
	RemoveEmpties(MyDir)
	ChangeDashAndSpaceToNothing(MyDir)
	ChangeShowNames(MyDir)
	CreateShowFolders(MyDir)
	MoveFiles(MyDir)

if __name__ == "__main__":
    DoTheLot()
