class FunctionRecord:
    def __init__(self, funName):
        self.functionName = funName
        self.frequency = 0
        self.cacheable = None
        self.callers = []
        self.args = None
        self.equal_args = True

    def isCacheable(self):
        return self.cacheable
    
    def increment_frequency(self):
        self.frequency += 1

    def add_caller(self, caller):
        self.callers.append(caller)

    def update_args(self, args):
        if self.args is None:
            self.args = args
        else:
            if self.args != args:
                self.equal_args = False
            else:
                self.equal_args = True

    def update_cacheable(self, returnValue):
        if self.frequency > 1 and self.cacheable is not None:
            if returnValue != self.cacheable or self.equal_args is False:
                self.cacheable = None
        else:
            self.cacheable = 1
        
    def print_report(self):
        cacheable_value = int(self.isCacheable()) if self.isCacheable() is not None else 0
        print("{:<30} {:<10} {:<10} {}".format(self.functionName, self.frequency, cacheable_value, self.callers))

    def __eq__(self, other):
        if isinstance(other, FunctionRecord):
            return self.functionName == other.functionName and self.frequency == other.frequency and self.isCacheable() == other.isCacheable() and self.callers == other.callers
        return False

    @classmethod
    def new_instance_with(cls, funName, frequency, cacheable, callers):
        instance = cls(funName)
        instance.frequency = frequency
        instance.cacheable = cacheable
        instance.callers = callers
        return instance