#! /usr/bin/env python3
import unittest
from star1 import Cave, PathFindingState

TEST1 = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''.splitlines()

TEST2 = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''.splitlines()

TEST3 = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''.splitlines()

class Test1(unittest.TestCase):
    def test1(self):
        c = Cave(TEST1)
        self.assertEqual(10, len(c.all_paths()))

    def test2(self):
        c = Cave(TEST2)
        self.assertEqual(19, len(c.all_paths()))

    def test3(self):
        c = Cave(TEST3)
        self.assertEqual(226, len(c.all_paths()))

STAR2_PATHS = '''start,A,b,A,b,A,c,A,end
start,A,b,A,b,A,end
start,A,b,A,b,end
start,A,b,A,c,A,b,A,end
start,A,b,A,c,A,b,end
start,A,b,A,c,A,c,A,end
start,A,b,A,c,A,end
start,A,b,A,end
start,A,b,d,b,A,c,A,end
start,A,b,d,b,A,end
start,A,b,d,b,end
start,A,b,end
start,A,c,A,b,A,b,A,end
start,A,c,A,b,A,b,end
start,A,c,A,b,A,c,A,end
start,A,c,A,b,A,end
start,A,c,A,b,d,b,A,end
start,A,c,A,b,d,b,end
start,A,c,A,b,end
start,A,c,A,c,A,b,A,end
start,A,c,A,c,A,b,end
start,A,c,A,c,A,end
start,A,c,A,end
start,A,end
start,b,A,b,A,c,A,end
start,b,A,b,A,end
start,b,A,b,end
start,b,A,c,A,b,A,end
start,b,A,c,A,b,end
start,b,A,c,A,c,A,end
start,b,A,c,A,end
start,b,A,end
start,b,d,b,A,c,A,end
start,b,d,b,A,end
start,b,d,b,end
start,b,end'''.splitlines()

class Test2(unittest.TestCase):
    def test1(self):
        c = Cave(TEST1)
        ap = c.all_paths(False)
        self.assertEqual(sorted(STAR2_PATHS), sorted(ap))
        self.assertEqual(36, len(ap))

    def test2(self):
        c = Cave(TEST2)
        self.assertEqual(103, len(c.all_paths(False)))

    def test3(self):
        c = Cave(TEST3)
        self.assertEqual(3509, len(c.all_paths(False)))


class Test0(unittest.TestCase):
    def testNoExtraVisit(self):
        extra_visit=True
        p = PathFindingState('start', extra_visit=True)
        p = PathFindingState('a', ['start'], extra_visit=True)
        self.assertEqual(['start','a'], p.path)
        p = PathFindingState('b', ['start', 'a'], extra_visit=True)
        p = PathFindingState('A', ['start', 'A', 'a'], extra_visit=True)
        with self.assertRaises(Exception):
            p = PathFindingState('a', ['start', 'a', 'b'], extra_visit=True)

    def testWithExtraVisit(self):
        p = PathFindingState('start', extra_visit=False)
        p = PathFindingState('a', ['start'], extra_visit=False)
        p = PathFindingState('b', ['start', 'a'], extra_visit=False)
        p = PathFindingState('a', ['start', 'a', 'b'], extra_visit=False)
        self.assertTrue(p.extra_visit)
        with self.assertRaises(Exception):
            p = PathFindingState('b', ['start', 'a', 'b', 'a'], extra_visit=True)

if __name__=='__main__':
    unittest.main()
