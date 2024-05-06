import sys
import ast
import inspect
from types import *
import traceback
from stack_inspector import StackInspector
from line_record import LineRecord

""" Clase para la Tarea 2. Para su uso, considere:
with CoverageTracer() as covTracer:
    function_to_be_traced()

covTracer.report_executed_lines()
"""

class CoverageTracer(StackInspector):

 
    def __init__(self):
        super().__init__(None, self.traceit)
        self.executed_lines = {} 

    def traceit(self, frame, event: str, arg):
        if self.our_frame(frame) or self.problematic_frame(frame):
            pass
        else:
            key = (frame.f_code.co_name, frame.f_lineno)
            if key not in self.executed_lines:
                self.executed_lines[key] = LineRecord(*key)
            else:
                self.executed_lines[key].increaseFrequency()
            return self.traceit
        
    def traceit(self, frame, event: str, arg):
        if self.our_frame(frame) or self.problematic_frame(frame):
            pass
        else:
            if event == "line":
                key = (frame.f_code.co_name, frame.f_lineno)
                if key not in self.executed_lines:
                    self.executed_lines[key] = LineRecord(*key)
                else:
                    self.executed_lines[key].increaseFrequency()
        return self.traceit

    def print_lines_report(self):
        print("{:<30} {:<10} {:<10}".format('fun', 'line', 'freq'))
        for line_record in self.executed_lines.values():
            line_record.print_report()

    def report_executed_lines(self):
        self.print_lines_report()
        sorted_lines = sorted(self.executed_lines.values(), key=lambda x: x.lineNumber)
        return sorted_lines