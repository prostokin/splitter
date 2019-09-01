# -*- coding: UTF-8 -*-
import os
import re
import subprocess


class Album:
    def __init__(self, path):
        self.path = path
        self.name = os.path.split(self.path)[1]
        self.cuePath = self.__getFileList(suffix="cue")[0]
        self.tracksCount = 0
        self.tracksList = []
        self.getAlbumData()
        self.splited = self.isSplited()

    def isSplited(self):
        self.tracksList += self.__getFileList(pattern=r"\d\d(\s|\w|\W)*", suffix="flac")
        if len(self.tracksList) == self.tracksCount or self.tracksCount == 1:
            return True
        else:
            return False

    def getAlbumData(self):
        cueFile = open(self.cuePath, 'r')
        for line in cueFile:
            if "FILE" in line:
                match = re.search(r"\"(\s|\w|\W)*\"", line)
                flacName = match.group(0)[1:-1]
                self.flacPath = os.path.join(self.path, flacName)
            if "TRACK" in line:
                self.tracksCount += 1
        cueFile.close()
        if self.tracksCount == 1:
            self.tracksList.append(self.flacPath)

    def __getFileList(self, pattern="", suffix=""):
        filePathList = [file.path for file in os.scandir(self.path) if file.is_file() and re.search(r"{0}({1})$".format(pattern, suffix), file.name)]
        return filePathList

    def tagFiles(self):
        os.chdir(self.path)
        args = ["cuetag.sh", self.cuePath]
        proc = subprocess.run(args + self.tracksList)
        if proc.returncode == 0:
            print("\nFiles tagged")
            return 0
        else:
            return 1

    def split(self, delFlac=False):
        if not self.splited:
            os.chdir(self.path)
            proc = subprocess.run(["shnsplit", "-f", self.cuePath, "-o", "flac",
                                     "-t", "%n_%t", self.flacPath])
            if proc.returncode == 0:
                self.tracksList = self.__getFileList(pattern=r"\d\d(\s|\w|\W)*", suffix="flac")
                if delFlac and self.flacPath:
                    self.__delFlac()
            else:
                return 1
        else:
            print("Already splitted")
            self.tracksList = self.__getFileList(pattern=r"\d\d(\s|\w|\W)*", suffix="flac")

    def __delFlac(self):
        if self.tracksCount != 1:
            proc = subprocess.run(["gio", "trash", self.flacPath])
            if proc.returncode == 0:
                print("\nFile: {0}\nmoved to trash".format(self.flacPath))
                self.flacPath = None
                return 0
            else:
                return 1


class Discography:
    def __init__(self, path):
        self.path = path
        self.albumsList = [Album(path) for path in self.__getPathList()]

    def __getPathList(self):
        pathList = []
        tree = os.walk(self.path)
        for path, dirs, files in tree:
            for file in files:
                if re.search(r"(.cue)$", file) and not path in pathList:
                    pathList.append(path)
        return pathList


def main(discoPath):
    if not os.path.exists(discoPath):
        print("Path: {} does not exists".format(discoPath))
        return
    else:
        disco = Discography(discoPath)
        if len(disco.albumsList) == 0:
            print("There are no albums in:\n{0}".format(disco.path))
        else:
            for album in disco.albumsList:
                print("{0} {1}".format(album.name, album.tracksCount))
                album.split(delFlac=True)
                album.tagFiles()


if __name__ == '__main__':
    main(os.getcwd())
    #some comments
    #some comments
    #some comments
    #some comments
    
