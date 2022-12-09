#! /usr/bin/env python3

import unittest
from star import parse, State, solve

DATA1='''#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #########'''.splitlines()

DATA2='''#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########'''.splitlines()


DATA3='''#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########'''.splitlines()

class Test1(unittest.TestCase):
    def testParse(self):
        state = parse(DATA1)
        self.assertEqual(state.state,'..........DABC.ABCD')

    def testNextMove(self):
        state = parse(DATA1)
        self.assertListEqual(list(state.possible_moves()), [(10, 14, 3000)])

    def testSolve(self):
        state = parse(DATA1)
        self.assertEqual(solve(state), 3000)

    def testSolve2(self):
        state = parse(DATA2)
        self.assertEqual(solve(state), 12521)


class Test2(unittest.TestCase):
    def testParse(self):
        state = parse(DATA3)
        self.assertEqual(state.state,'...........BCBDDCBADBACADCA')

    def testParse2(self):
        state1 = parse(DATA2, inject_extra=True)
        state2 = parse(DATA3)
        self.assertEqual(state2.state, state1.state)

    def testSolve(self):
        state = parse(DATA2, inject_extra=True)
        self.assertEqual(solve(state), 44169)

if __name__=='__main__':
    unittest.main()
