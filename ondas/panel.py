

class Panel():
    def __init__(self,size,name,color(10,10,10,100)):
        self.size =(900,200)
        self.position = (0,0)
        self.panel_color = color
        self.type =  name
        self.focus = False
        self.panel = pygame.Surface(self.size).convert_alpha()
        self.panel.fill(self.panel_color)
        self.time = 0
        self.step = 1
