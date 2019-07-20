# -*- coding: UTF-8 -*-
import os
import re
import subprocess
import sys


def getDirList(rootDirPath):
    print(rootDirPath)
    return os.walk(rootDirPath)


def getCuesList(dirList):
    pattern = r".cue"
    cueList = []

    for entry in dirList:
        added = False
        for fileName in entry[2]:
            if re.search(pattern, fileName) and not added:
                cueList.append(os.path.join(entry[0], fileName))
                added = True
    return cueList


def splitFiles(cueList):
    for cueFilePath in cueList:
        currentDirPath = os.path.split(cueFilePath)[0]
        flacFilePath = cueFilePath.split('.')[0] + '.flac'
        os.chdir(currentDirPath)
        print(os.getcwd())
        subprocess.run(["shnsplit", "-f", cueFilePath, "-o", "flac", "-t", "%n %t", flacFilePath])
        subprocess.run(["gio", "trash", flacFilePath])
        subprocess.run(["cuetag.sh", cueFilePath, "*.flac"])

def main(rootDirPath):
    dirList = getDirList(rootDirPath)
    splitFiles(getCuesList(dirList))


if __name__ == '__main__':
    main(sys.argv[1])
