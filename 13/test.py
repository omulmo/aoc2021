#! /usr/bin/env python3

import unittest
from star import Paper

TESTDATA = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5'''.splitlines()

class Test1(unittest.TestCase):
    def test1(self):
        p = Paper(TESTDATA)
        self.assertEqual(18, p.stars())
        p.fold(1)
        self.assertEqual(17, p.stars())
        pass


class Test2(unittest.TestCase):
    def test1(self):
        pass

if __name__=='__main__':
    unittest.main()
