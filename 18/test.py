#! /usr/bin/env python3

import unittest
from star import parse, try_explode, try_split, reduce, add

TESTDATA_1 = '''[1,1]
[2,2]
[3,3]
[4,4]'''.splitlines()

TESTDATA_2 = '''[1,1]
[2,2]
[3,3]
[4,4]
[5,5]'''.splitlines()

TESTDATA_3 = '''[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]'''.splitlines()

TESTDATA_4 = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''.splitlines()

TESTDATA_5 = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''.splitlines()

class Test0(unittest.TestCase):
    def testParse(self):
        q = '[[[[0,7],4],[15,[0,13]]],[1,1]]'
        self.assertEqual(q, str(parse(q)))
    def testSplit(self):
        sf = parse('[11,10]')
        self.assertTrue(try_split(sf))
        self.assertEqual('[[5,6],10]', str(sf))
        self.assertTrue(try_split(sf))
        self.assertEqual('[[5,6],[5,5]]', str(sf))
    def testSplit1(self):
        q = '[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'
        sf = parse(q)
        self.assertFalse(try_split(sf))
        self.assertEqual(q, str(sf))
    def testSplit2(self):
        sf = parse('[[[[0,7],4],[[7,8],[0,13]]],[1,1]]')
        self.assertTrue(try_split(sf))
        self.assertEqual('[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]', str(sf))

class Test1(unittest.TestCase):
    def doExplode(self, a, b, should_explode=True):
        sf = parse(a)
        self.assertEqual(should_explode, try_explode(sf))
        self.assertEqual(b if should_explode else a, str(sf))
    def testExplode1(self):
        self.doExplode('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
    def testExplode2(self):
        self.doExplode('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
    def testExplode3(self):
        self.doExplode('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]')
    def testExplode(self):
        self.doExplode('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
    def testExplode(self):
        self.doExplode('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

class Test2(unittest.TestCase):
    def testReduce(self):
        self.assertEqual('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', str(reduce(parse('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]'))))

class Test3(unittest.TestCase):
    def test1(self):
        self.assertEqual('[[[[1,1],[2,2]],[3,3]],[4,4]]', str(add(TESTDATA_1)))

    def test2(self):
        self.assertEqual('[[[[3,0],[5,3]],[4,4]],[5,5]]', str(add(TESTDATA_2)))

    def test3(self):
        self.assertEqual('[[[[5,0],[7,4]],[5,5]],[6,6]]', str(add(TESTDATA_3)))

    def test4(self):
        self.assertEqual('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]', str(add(TESTDATA_4)))

class Test4(unittest.TestCase):
    def test6(self):
        self.assertEqual(143, parse('[[1,2],[[3,4],5]]').magnitude())

    def test7(self):
        self.assertEqual(1384, parse('[[[[0,7],4],[[7,8],[6,0]]],[8,1]]').magnitude())

    def test8(self):
        self.assertEqual(1137, parse('[[[[5,0],[7,4]],[5,5]],[6,6]]').magnitude())

    def test9(self):
        self.assertEqual(3488, parse('[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]').magnitude())

    def test9(self):
        self.assertEqual(4140, add(TESTDATA_5).magnitude())

if __name__=='__main__':
    unittest.main()
