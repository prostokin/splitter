# -*- coding: UTF-8 -*-
import os
import re
import subprocess
import sys


class Album:
    def __init__(self, path):
        self.path = path
        self.name = os.path.split(self.path)[1]
        # self.updateFileList()
        self.fileList = self.__getFileList()
        self.flacPathList = self.__getFileList(suffix="flac")
        self.cuePathList = self.__getFileList(suffix="cue")
        self.__delCueDuplicates()
        self.cdsCount = len(self.flacPathList)
        self.getAlbumData()
        # self.tracksCount = self.__getTracksCount()
        # self.splited = self.__getSplited()

    def __repr__(self):
        info = str("Name: {0}\n".format(self.name) +
        "Path: {0}\n".format(self.path) +
        "CDs: {0}\n".format(self.cdsCount) +
        "Tracks: {0}\n".format(self.tracksCount) +
        "Splited: {0}\n".format(self.splited) +
        "CUE: {0}\n".format(self.cuePath) +
        "Flac: {0}\n".format(self.flacPath))
        return info

    def __delCueDuplicates(self):
        for currentPath in self.cuePathList:
            currentName = os.path.split(currentPath)[1].split(".")[0]
            for path in self.cuePathList:
                name = os.path.split(path)[1].split(".")[0]
                if currentPath != path and currentName == name:
                    self.cuePathList.remove(path)

    def getAlbumData(self):
        self.data = {}
        for cuePath in self.cuePathList:
            self.data[cuePath] = [self.flacPathList[self.cuePathList.index(cuePath)]]
            # поиск по индексу это фуфло)

    # def __getSplited(self):
    #     flacList = [file for file in self.fileList if re.search(r"(flac)$", file.name)]
    #     if len(flacList) >= self.tracksCount:
    #         return True
    #     else:
    #         return False

    # def __getTracksCount(self):
    #     count = 0
    #     cue = open(self.cuePath, "r")
    #     for line in cue:
    #         if "TRACK" in line:
    #             count += 1
    #     cue.close()
    #     return count

    # def updateFileList(self):
    #     self.fileList = self.__getFileList()

    # def __getFlacList(self):
    #     self.updateFileList()
    #     flacList = [file.name for file in self.fileList if re.search(r"\d\d(\s|\w|\W)*(flac)$", file.name)]
    #     return flacList

    def __getFileList(self, pattern="", suffix=""):
        filePathList = [file.path for file in os.scandir(self.path) if file.is_file() and re.search(r"{0}({1})$".format(pattern, suffix), file.name)]
        return filePathList

    # def tagFiles(self):
    #     if self.flacPath:
    #         self.__delFlac()
    #     os.chdir(self.path)
    #     args = ["cuetag.sh", self.cuePath]
    #     proc = subprocess.run(args + self.__getFlacList())
    #     if proc.returncode == 0:
    #         print("\nFiles tagged")
    #         return

    # def split(self):
    #     if not self.splited:
    #         os.chdir(self.path)
    #         proc = subprocess.run(["shnsplit", "-f", self.cuePath, "-o", "flac",
    #                                  "-t", "%n_%t", self.flacPath])
    #         if proc.returncode == 0:
    #             self.splited = True
    #             return 0
    #         else:
    #             return 1
    #     else:
    #         print("\nAlbum: {0} has already splited".format(self.name))
    #         return

    # def __delFlac(self):
    #     proc = subprocess.run(["gio", "trash", self.flacPath])
    #     if proc.returncode == 0:
    #         print("\nFile: {0}\nmoved to trash".format(self.flacPath))
    #         self.flacPath = None
    #         return 0
    #     else:
    #         return 1


class Discography:
    def __init__(self, path):
        self.path = path
        self.albumsList = []

    def getAlbumsList(self):
        pass


def main(discoPath):
    # disco = Discography(discoPath)
    # print(disco.path)

    # album = Album(r"/run/media/pavel/Новый том/Multimedia/Music/Agalloch/2011-Whitedivisiongrey"))
    album = Album(r"/run/media/pavel/Новый том/Multimedia/Music/Agalloch/2002-The Mantle")
    print(album.name)
    print(album.path)

    # for path in album.cuePathList:
    #     print(path)
    print(album.data)
    # album.split()
    # album.tagFiles()


if __name__ == '__main__':
    path = r"/run/media/pavel/Новый том/Multimedia/Music/Agalloch"
    main(path)
