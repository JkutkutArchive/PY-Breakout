from Classes.color import *;

class Player():
    def __init__(self, x, screenW, screenH) -> None:
        self._x = x

        self.screenW = screenW
        self.screenH = screenH

        self.unit = self.screenW // 50

        self._color = color().WHITE


    # GETTERS

    def color(self):
        return self._color
    
    def getBodyShape(self):
        return [
            (self._x - self.unit * 2.5, self.screenH),
            (self._x + self.unit * 2.5, self.screenH),

            (self._x + self.unit * 3.5, self.screenH - self.unit),
            (self._x - self.unit * 3.5, self.screenH - self.unit)
        ]