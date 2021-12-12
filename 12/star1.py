from collections import defaultdict
from copy import deepcopy
from os import path
import sys


class PathFindingState:
    def __init__(self, curr, path=[], extra_visit=False):
        if curr.lower() == curr and curr in path:
            if extra_visit: raise Exception
            extra_visit = True
        self.curr = curr
        self.path = deepcopy(path)
        self.path.append(curr)
        self.extra_visit = extra_visit
    
    def __hash__(self):
        return hash(f'{self.curr}:{self.path}:{self.extra_visit}')


class Cave:
    def __init__(self, inputs):
        self.paths = defaultdict(lambda: [])
        for line in inputs:
            src,dst = line.strip().split('-')
            if dst != 'start':
                self.paths[src].append(dst)
            if src != 'start':
                self.paths[dst].append(src)


    def all_paths(self, extra_visit_spent=True):
        all_paths = set()
        candidates = [ PathFindingState('start', extra_visit=extra_visit_spent) ]
        already_tried_this = set()
        while len(candidates)>0:
            state = candidates.pop()
            h = hash(state)
            if h in already_tried_this: continue
            already_tried_this.add(h)
            if state.curr == 'end':
                all_paths.add(','.join(state.path))
                continue
            for target in self.paths[state.curr]:
                try:
                    new_state = PathFindingState(target, state.path, state.extra_visit)
                    candidates.append(new_state)
                except:
                    pass
        return all_paths


if __name__=='__main__':
    extra_visit_spent = 1 == int('1' if len(sys.argv)<2 else sys.argv[1])
    print(len(Cave(sys.stdin).all_paths(extra_visit_spent)))
