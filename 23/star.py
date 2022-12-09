#! /usr/bin/env python3
from collections import defaultdict
from sortedcontainers import SortedSet
from collections.abc import Iterable
from enum import Enum
from typing import Iterator, Optional
import sys

Coord = tuple[int,int]

class _PathState:
    def __init__(self, path:list[Coord], cost) -> None:
        self.path = path
        self.cost = cost
    def next(self, world:list[Coord]) -> Iterator['_PathState']:
        x,y = self.path[-1]
        return (_PathState(self.path+[nbor], self.cost+1) for nbor in ((x+1,y),(x-1,y),(x,y-1),(x,y+1)) if nbor in world)

def best_path(world:list[Coord], start:Coord, dest:Coord) -> _PathState:
    best = _PathState([], sys.maxsize)
    candidates: set[_PathState] = SortedSet([_PathState([start],0)], key=lambda x:x.cost)
    while len(candidates)>0:
        candidate:_PathState = candidates.pop(0)
        if candidate.cost > best.cost:
            break
        last = candidate.path[-1]
        if last == dest and candidate.cost < best.cost:
            best = candidate
            continue
        for next in candidate.next(world):
            candidates.add(next)
    return best

Id = int
Trail = list[Id]
FromTo = tuple[Id,Id]

class Board:
    def __init__(self, world:list[Coord]):
        self.hallway : list[Id] = []
        self.homes : dict[str,list[Id]] = {}
        self.trails : dict[FromTo,Trail] = {}
        self.size = len(world)

        is_hallway = lambda pos: pos[1]==1
        is_restricted = lambda pos: is_hallway(pos) and (pos[0],pos[1]+1) in world

        pos_to_id : dict[Coord,Id] = {}
        for id,pos in enumerate(world):
            pos_to_id[pos] = id

        for pos in world:
            if is_hallway(pos):
                if not is_restricted(pos):
                    self.hallway.append(pos_to_id[pos])
            else:
                letter = chr(ord('A') + (pos[0]-3)//2)
                self.homes[letter] = arr = self.homes.get(letter, [])
                arr.append(pos_to_id[pos])

        for i in range(self.size):
            for j in range(self.size):
                if i==j: continue
                best = best_path(world,world[i],world[j])
                self.trails[i,j] = list(map(lambda pos:pos_to_id[pos], best.path))[1:]

    def target_state(self) -> str:
        state = ['.']*self.size
        for letter in self.homes:
            for id in self.homes[letter]:
                state[id] = letter
        return ''.join(state)

    def ok_to_move_home(self, state:str, kind:str) -> bool:
        acceptable = '.'+kind
        return all([state[i] in acceptable for i in self.homes[kind]])

    def move_home(self, state:str, kind:str) -> Id:
        for i in reversed(self.homes[kind]):
            if state[i]=='.': return i
        raise Exception()

    def can_move(self, state:str, pos:Id, dest:Id) -> int:
        trail = self.trails[pos,dest]
        return len(trail) if all(state[id]=='.' for id in trail) else -1

    def estimated_cost(self, state:str) -> int:
        cost=0
        for id,kind in enumerate(state):
            if kind=='.' or id in self.homes[kind]: continue
            dest=next((id for id in reversed(self.homes[kind]) if state[id]=='.'), self.homes[kind][-1])
            cost += len(self.trails[id,dest]) * ENERGY[kind]
        return cost


Energy = int

ENERGY: dict[str,Energy] = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

class Action(Enum):
    MoveToHallway=1
    Waiting=2
    MoveToHome=3
    Done=4

Move = tuple[Id,Id,Energy]

def calc_possible_moves(board:Board, state:str, pos:Id) -> Iterable[Move]:
    kind = state[pos]
    energy = ENERGY[kind]
    home_ok = board.ok_to_move_home(state, kind)
    if pos in board.homes[kind]:
        action = Action.Done if home_ok else Action.MoveToHallway
    elif pos in board.hallway:
        action = Action.MoveToHome if home_ok else Action.Waiting
    else:
        action = Action.MoveToHallway

    destinations = []
    match action:
        case Action.Done:
            return
        case Action.Waiting:
            return
        case Action.MoveToHallway:
            destinations = board.hallway
        case Action.MoveToHome:
            destinations = [board.move_home(state,kind)]
        case _:
            raise Exception()

    for dest in destinations:
        steps = board.can_move(state, pos, dest)
        if steps < 0: continue
        yield pos,dest,steps*energy




class State:
    def __init__(self, board:Board, state:str, cost:int):
        self.board = board
        self.state = state
        self.cost = cost
        self.heur = cost + board.estimated_cost(state)

    def __repr__(self) -> str:
        return f'{self.state} ({self.cost} -> {self.heur})'

    def possible_moves(self) -> Iterable[Move]:
        result = []
        for id,cell in enumerate(self.state):            
            if cell=='.': continue
            result.extend(calc_possible_moves(self.board, self.state, id))
        return result

    def move(self, move:Move):
        copy = [ i for i in self.state ]
        src,dest,cost = move
        copy[dest]=copy[src]
        copy[src]='.'
        return State(self.board, ''.join(copy), self.cost+cost)

def parse(inputs:list[str], inject_extra=False) -> State:
    if inject_extra:
        last2 = [inputs.pop(), inputs.pop()]
        inputs.append('  #D#C#B#A#')
        inputs.append('  #D#B#A#C#')
        inputs.append(last2.pop())
        inputs.append(last2.pop())

    coords:list[Coord] = []
    initial_state = []
    for y,row in enumerate(inputs):
        for x,cell in enumerate(row):
            if cell in 'ABCD.':
                coords.append((x,y))
                initial_state.append(cell)

    return State(Board(coords), ''.join(initial_state),0)


def solve(start:State) -> int:
    target_state = start.board.target_state()
    lowest_cost = sys.maxsize
    visited : dict[str, int] = defaultdict(lambda:sys.maxsize)
    candidates = SortedSet([start], key=lambda state:state.heur)
    while len(candidates)>0:
        next:State = candidates.pop(0)
        if next.cost > lowest_cost:
            break
        state = next.state
        if visited[state] < next.cost:
            continue
        visited[state] = next.cost
        if state == target_state:
            lowest_cost = min(lowest_cost, next.cost)
        for move in next.possible_moves():
            candidates.add(next.move(move))

    return visited[target_state]

if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]
    inputs = [ line for line in sys.stdin ]
    print(solve(parse(inputs, True if mode=='2' else False)))