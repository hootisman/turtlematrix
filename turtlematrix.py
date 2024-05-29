from foundrymatrix.base import MatrixBase
from foundrymatrix.input import MatrixUserInput
from rgbmatrix import graphics
import time
import math

running = True
segs = []

class Drawn(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = graphics.Color(255,255,0)

    def draw(self,matrix):
        graphics.DrawLine(matrix,self.x1, self.y1, self.x2, self.y2, self.color)
        

class Turtle(object):
    def __init__(self):
        self.x = 32
        self.y = 32
        self.tx = self.x
        self.ty = self.y
        self.t = 1
        self.color = graphics.Color(0,255,255)
        self.speed = 0.1
        self.rotation = 0   #in radians
        
        self.input = MatrixUserInput()
        self.input.attach_key('q', self.stop)

    def delay(self):
        time.sleep(2)

    def draw(self, matrix):


        if self.t <= 1:
            global segs
            x = self.lerp(self.x, self.tx, self.t)
            y = self.lerp(self.y, self.ty, self.t)
            seg = segs[0]
            seg.x2 = x
            seg.y2 = y

            self.t += 0.1
            if self.t >= 1:
                self.x = self.tx
                self.y = self.ty
        else:
            x = self.x
            y = self.y
        graphics.DrawLine(matrix,x, y, x, y, self.color)
    
    def lerp(self, start, end, t):
        return (1 - t) * start + t * end

    def forward(self,amt):
        global segs

        self.tx = math.floor(self.x + amt * math.cos(self.rotation))
        self.ty = math.floor(self.y + amt * math.sin(self.rotation))
        
        self.t = 0
        segs.insert(0, Drawn(self.x, self.y, self.x, self.y))

        self.delay()
    
    def rot(self, rad):
        self.rotation = rad

    # User Input Functions
    def stop(self):
        global running
        running = False
        self.input.exit()

class TurtleMatrix(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(TurtleMatrix, self).__init__(*args, **kwargs)
    
    def run(self):
        global running, segs
        color = graphics.Color(255,0,255)

        turt = Turtle()
        turt.rot(63)
        turt.forward(20)
        while running:
            
            for seg in segs:
                seg.draw(self.matrix)

            turt.draw(self.matrix)
            
            time.sleep(turt.speed)
            print("x ", turt.x, "y ", turt.y, "tx ", turt.tx, "ty ", turt.ty, "t ", turt.t)
            self.clear_screen()

if __name__ == "__main__":
    runnable = TurtleMatrix()
    if (not runnable.process()):
        runnable.print_help()
