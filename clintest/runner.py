import clingo
from .model import *

class Runner:
    ctls = {
        "clingo": clingo.Control
    }


    def __init__(self, function, argument, encoding, instance, folder =""):
        self.function = function
        self.argument = argument
        self.encoding = encoding + instance
        self.folder = folder

    def from_json(json):
        if 'instance' in json:
            instance = []
        else:
            instance = json['instance']
        runner = Runner(function=json['function'],
                        argument=json['argument'],
                        encoding=json['encoding'],
                        instance=instance,
                        folder = json['folder'])
        return runner

    def run(self, callbacks):

        on_model_cb = [c for c in callbacks if c.type=="on_model"]
        on_finish_cb = [c for c in callbacks if c.type=="on_finish"]
        try:
            ctl = self.ctls[self.function](self.argument)
        except:
            raise "Control object not recognized"

        for p in self.encoding:
            ctl.load(self.folder + p)

        ctl.ground([("base", [])])
        result_handle = []
        print('SOLVER CALL RESULT\n')
        with ctl.solve(yield_=True) as handle:
            for m in handle:
                print("-", m)
                model = Model.from_model(m)
                for c in on_model_cb:
                    c(model)

            
            sr = handle.get()
            for c in on_finish_cb:
                c(sr)

        result = []
        print('\nCLINTEST RESULT\n')
        for rh in on_finish_cb + on_model_cb:
            result = rh.conclude()
            result.addrunner(self)
            print(result)

    def __str__(self):
        ret = f"{self.function}, arguments : '{str(self.argument)}', encodings : {str(self.encoding)}\n"
        return ret
        

            


    
