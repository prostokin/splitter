# -*- coding: UTF-8 -*-
import os
import re
import subprocess
import sys


class Album:
    def __init__(self, path):
        self.path = path
        self.name = os.path.split(self.path)[1]
        self.fileList = [entry for entry in os.scandir(self.path) if entry.is_file()]
        self.cuePath = self.__getCuePath()
        self.cdsCount = self.__getCdsCount()
        self.tracksCount = self.__getTracksCount()
        self.splited = self.__getSplited()

    def __repr__(self):
        return "Name: {0}\nPath: {1}\nCDs: {2}\nSplited: {3}\nCUE: {4}\nTracks: {5}".format(self.name, self.path, 
                                                                    self.cdsCount, self.splited,
                                                                    self.cuePath, self.tracksCount)

    def __getSplited(self):
        if len(self.fileList) >= self.tracksCount:
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

    def __getCuePath(self):
        for entry in self.fileList:
            if re.search(r"(cue)$", entry.name):
                cuePath = entry.path
                return cuePath


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


if __name__ == '__main__':
    path = r"/run/media/pavel/Новый том/Multimedia/Music/Agalloch"
    main(path)
