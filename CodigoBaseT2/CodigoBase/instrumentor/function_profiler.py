from abstract_profiler import Profiler
from function_instrumentor import *
from function_record import FunctionRecord

# Clase que rastrea y reporta las funciones que se ejecutan
class FunctionProfiler(Profiler):

    # Metodo que se llama cada vez que se ejecuta una funcion
    @classmethod
    def record_start(cls, functionName, args):
        cls.getInstance().fun_call_start(functionName, args)

    @classmethod
    def record_end(cls, functionName, returnValue):
        cls.getInstance().fun_call_end(functionName, returnValue)
        return returnValue

    # Este metodo inyecta codigo en el programa segun el visitor del profiler
    @classmethod
    def instrument(cls, ast):
        visitor = FunctionInstrumentor()
        return fix_missing_locations(visitor.visit(ast))
    
    # Metodos de instancia
    def __init__(self):
        self.records = {}
        self.lastFuntionCalled = ""

    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    def fun_call_start(self, functionName, args):  
        record = self.get_record(functionName)
        record.increment_frequency()
        record.update_args(args)
        if self.lastFuntionCalled != "":
            record.add_caller(self.lastFuntionCalled)
        self.lastFuntionCalled = functionName

    def fun_call_end(self, functionName, returnValue):
        self.lastFuntionCalled = ""
        record = self.get_record(functionName)
        record.update_cacheable(returnValue)
        

    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10}".format('fun', 'freq', 'cache', 'callers'))
        for record in self.records.values():
            record.print_report()
        
    def report_executed_functions(self):
        self.print_fun_report()
        return self.records
