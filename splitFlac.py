# -*- coding: UTF-8 -*-
import os
import re
import subprocess
import sys


class Album:
    def __init__(self, path):
        self.path = path
        self.name = os.path.split(self.path)[1]
        self.updateFileList()
        self.cuePath = self.__getFilePath("cue")
        self.flacPath = self.__getFilePath("flac")
        self.cdsCount = self.__getCdsCount()
        self.tracksCount = self.__getTracksCount()
        self.splited = self.__getSplited()

    def __repr__(self):
        info = str("Name: {0}\n".format(self.name) +
        "Path: {0}\n".format(self.path) +
        "CDs: {0}\n".format(self.cdsCount) +
        "Tracks: {0}\n".format(self.tracksCount) +
        "Splited: {0}\n".format(self.splited) +
        "CUE: {0}\n".format(self.cuePath) +
        "Flac: {0}\n".format(self.flacPath))
        return info

    def __getSplited(self):
        flacList = [file for file in self.fileList if re.search(r"(flac)$", file.name)]
        if len(flacList) >= self.tracksCount:
            return True
        else:
            return False

    def __getCdsCount(self):
        count = 0
        for entry in self.fileList:
            if re.search(r"(CD)(\s|\w|\W)*(flac)$", entry.name):
                count += 1
        if count:
            return count
        else:
            return 1

    def __getTracksCount(self):
        count = 0
        cue = open(self.cuePath, "r")
        for line in cue:
            if "TRACK" in line:
                count += 1
        cue.close()
        return count

    def updateFileList(self):
        self.fileList = [entry for entry in os.scandir(self.path) if entry.is_file()]

    def __getFlacList(self):
        self.updateFileList()
        flacList = [file.name for file in self.fileList if re.search(r"\d\d(\s|\w|\W)*(flac)$", file.name)]
        return flacList

    def __getFilePath(self, suffix):
        for entry in self.fileList:
            if re.search(r"({0})$".format(suffix), entry.name):
                cuePath = entry.path
                return cuePath

    def tagFiles(self):
        if self.flacPath:
            self.__delFlac()
        os.chdir(self.path)
        args = ["cuetag.sh", self.cuePath]
        proc = subprocess.run(args + self.__getFlacList())
        if proc.returncode == 0:
            print("\nFiles tagged")
            return

    def split(self):
        if not self.splited:
            os.chdir(self.path)
            proc = subprocess.run(["shnsplit", "-f", self.cuePath, "-o", "flac",
                                     "-t", "%n_%t", self.flacPath])
            if proc.returncode == 0:
                self.splited = True
                self.tagFiles()
                return 0
            else:
                return 1
        else:
            print("\nAlbum: {0} has already splited".format(self.name))
            return

    def __delFlac(self):
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
        self.albumsList = []

    def getAlbumsList(self):
        pass


def main(discoPath):
    # disco = Discography(discoPath)
    # print(disco.path)

    album = Album(r"/run/media/pavel/Новый том/Multimedia/Music/Agalloch/2002-The Mantle")
    print(album)
    print(album.split())
    # os.chdir(album.path)
    # album.tagFiles()


if __name__ == '__main__':
    path = r"/run/media/pavel/Новый том/Multimedia/Music/Agalloch"
    main(path)
