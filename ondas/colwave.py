import pygame
import math



class ColWave:
    def __init__ (self):
        self.size =(900,200)
        self.points = [(x,int(self.size[1]/2)) for x in range(self.size[0])]
        self.start = False
        self.position = (0,0)
        self.panel_color = (35,45,65,50)
        self.waves1 = list()
        self.waves2 = list()
        self.over_other_panel = False
        self.type = 'ColWave'
        self.focus = False
        self.panel = pygame.Surface(self.size).convert_alpha()
        self.panel.fill(self.panel_color)
        self.time = 0
        self.step = 1
    def update(self):
        self.clean()
        self.draw()
        self.timer()
    def Y_left (self,x,t):
        Y=0
        for i in self.waves2:
            Y += i.A*math.sin(i.w*t + i.k*x + i.teta)
        Y-=self.size[1]/2
        return -Y

    def Y_right (self,x,t):
            Y=0
            for i in self.waves2:
                Y += i.A*math.sin(i.w*self.time + i.k*x + i.teta)
            Y-=self.size[1]/2
            return -Y

    def timer (self):
        self.time += self.step
    def clean(self):
        self.panel.fill(self.panel_color)
    def add_waves (self, wave, team):
        if team == '1':
            self.waves1.append(wave)
        else:
            self.waves2.append(wave)

    def draw(self):
        my = self.size[1]/2
        mx = self.size[0]/2

            #---focus---#
        if self.focus:
            pygame.draw.circle(self.panel,(0,255,0),(10,10),3,0)
        else:
            pygame.draw.circle(self.panel,(255,0,0),(10,10),3,0)


        pygame.draw.rect(self.panel,(255,0,0),(0,0,self.size[0],self.size[1]),1)
        pygame.draw.line(self.panel,(255,255,255),(0,my),(self.size[0],my),1)
        pygame.draw.line(self.panel,(255,255,255),(mx,0),(mx,self.size[1]),1)

        for i in range(0,self.size[0],10):
            pygame.draw.line(self.panel,(255,255,255),(i,my-3),(i,my+3),1)
        for i in range(0,self.size[1],10):
            pygame.draw.line(self.panel,(255,255,255),(mx-3,i),(mx+3,i),1)

        if self.start:
            for i,wave1 in enumerate(self.points):
                Y = self.Y_right(self.size[0]-i)
