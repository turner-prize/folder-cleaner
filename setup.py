import os

#to automate some test files

dirpath = os.getcwd()
newpath = os.path.join(dirpath,'test-folder')

if not os.path.isdir(newpath):
    os.mkdir(newpath)

for i in range(1,20):
    for j in range(1,24):
        open (os.path.join(newpath,"TestShow.S{:02d}E{:02d}.mkv".format(j,i)),"w")
        open (os.path.join(newpath,"TestShow2.S{:02d}E{:02d}.mkv".format(j,i)),"w")
        open (os.path.join(newpath,"TestShow3.S{:02d}E{:02d}.mkv".format(j,i)),"w")
        open (os.path.join(newpath,"TestShow4.S{:02d}E{:02d}.screener.1060.mkv".format(j,i)),"w")
        open (os.path.join(newpath,"TestShow4.S{:02d}E{:02d}.screener.1060.mkv".format(j,i)),"w")