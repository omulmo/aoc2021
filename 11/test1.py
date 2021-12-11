#! /usr/bin/env python3
import unittest
from star1 import Cave

TEST1_0 = '''11111
19991
19191
19991
11111'''.splitlines()

TEST1_1 = '''34543
40004
50005
40004
34543'''.splitlines()

TEST1_2 = '''45654
51115
61116
51115
45654'''.splitlines()

TEST2_0 = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526'''.splitlines()

TEST2_10 = '''0481112976
0031112009
0041112504
0081111406
0099111306
0093511233
0442361130
5532252350
0532250600
0032240000'''.splitlines()

class Test1(unittest.TestCase):
    def test1(self):
        c = Cave(TEST1_0)
        c.step()
        self.assertEqual('\n'.join(TEST1_1), c.view())
        self.assertEqual(9, c.flashes)
        c.step()
        self.assertEqual(9, c.flashes)
        self.assertEqual(2, c.iterations)
        self.assertEqual('\n'.join(TEST1_2), c.view())

    def test2(self):
        c = Cave(TEST2_0)
        c.step(10)
        self.assertEqual(10, c.iterations)
        self.assertEqual(204, c.flashes)
        self.assertEqual('\n'.join(TEST2_10), c.view())

    def test3(self):
        c = Cave(TEST2_0)
        self.assertEqual(195, c.time_to_synchronize())

if __name__=='__main__':
    unittest.main()
