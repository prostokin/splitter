import unittest
from splitFlac import Album


class TestClass01(unittest.TestCase):
    path = r"/run/media/pavel/Drive/Multimedia/Music/Dolphin/2000-Плавники/"
    album = Album(path)

    def test_case01(self):        
        print("\n{0} {1}".format(self.album.name, self.album.tracksCount))
        print(self.album.flacPath)
        print(self.album.tracksList)
        print(self.album.splited)

    def test_case02(self):
        self.album.split()


if __name__ == '__main__':
    unittest.main(verbosity=2)
