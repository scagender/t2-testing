from __future__ import print_function
import threading
from time import sleep
import traceback
from sys import _current_frames


class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.tree = {}

        
    def start(self):
        self.active = True
        self.t.start()

    def stop(self):
        self.active = False
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                self.update__tree(stack)
                ##print(stack)
    
    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)

    def print_report(self):
        self.print_tree(self.tree)

    def print_tree(self, node, indent=0):
        for func_name, data in node.items():
            print('  ' * indent + f'{func_name}({data["tiempo"]} seconds)')
            self.print_tree(data['hijos'], indent + 1)

    def update__tree(self, stack):
        node = self.tree
        for func_name in stack:
            if func_name not in node:
                node[func_name] = {'tiempo': 1, 'hijos': {}}
            else:
                node[func_name]['tiempo'] += 1
            node = node[func_name]['hijos']
