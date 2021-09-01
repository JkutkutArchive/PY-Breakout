def constant(f): #define of a constant class
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)


class color(object): #Create the COLOR class as a collection of constants
    @constant
    def BG(): # background
        return (25, 25, 25) 
    @constant
    def GREY():
        return (128, 128, 128)
    @constant
    def GREYBORDER():
        return (188, 188, 188)
    @constant
    def WHITE():
        return (255, 255, 255)
    @constant
    def BLACK():
        return (0, 0, 0)