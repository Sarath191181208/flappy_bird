import time 

class Timer():
    def __init__(self,time,func = None, loop=False) -> None:
        self.current = 0
        self.time = time
        self.start_time = 0
        self.start = False
        self.func = func
        self.loop = loop

    def update(self):
        if self.start:
            self.current = time.time()
            if abs(self.current-self.start_time) >= self.time:
                self.reset()
    
    def start_timer(self):
        self.start = True
        self.start_time = time.time()
    
    def reset(self):
        self.start = False
        self.current = 0
        if self.func is not None:
            self.func()
        if self.loop:
            self.start_timer()