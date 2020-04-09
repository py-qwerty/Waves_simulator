import math
import pygame

pygame.init()

def write (panel,string, pos, size=10, color =[255,255,255],font ="Arial",boolean = False):
		font = pygame.font.SysFont(font,size)
		text = font.render(str(string),boolean,color)
		panel.blit(text, pos)

class Wave:
	def __init__(self, amplitude, period, longitude,teta =0,direc = 1):
			self.size = (600, 330)
			self.bottom = self.size[1]-60
			self.right = self.size[0]-100
			self.scale = float(1/10)   # 1cm por cada 10px
			self.size_graph = (500, 200)
			self.panel_color = (35,45,65,50)
			self.panel = pygame.Surface(self.size).convert_alpha()
			self.focus = False
			self.over_other_panel = False
			self.position = (0,0)
			self.panel.fill(self.panel_color)
			self.points = [(x,int(self.bottom/2)) for x in range(0,self.right,2)]
			self.rect = pygame.Rect(self.position[0],self.position[1],self.size[0],self.size[1])
			self.over_other_panel = False
			self.type = 'Wave'
			self.T = float(period)
			self.l = float(longitude)
			self.A = float(amplitude)
			self.f = float(1/self.T)
			self.v = float(self.l/self.scale/self.T)
			self.k = float(math.pi*2*self.scale/self.l)
			self.w = float(math.pi*2/self.T)
			self.time = 0
			self.teta = teta
			self.stop = False # Estado
			self.step = 2
			self.weight = 2
			self.dir = direc
			self.others_waves = list()
	def join_points (self,p1,p2):
	        pygame.draw.line(self.panel, (255,255,255),p1,p2, self.weight)


	def posY (self, x,t):
		V = int(self.w*(self.A/self.scale)*math.cos(self.w*t + self.dir*self.k*x + math.pi*self.teta))
		Y = int((self.A/self.scale)*math.sin(self.w*t + self.dir*self.k*x + math.pi*self.teta))
		if len(self.others_waves):
			for i in self.others_waves:
				if i.scale == self.scale:
					Y2 = i.posY(x,t)[0]
					V2 = i.posY(x,t)[1]
					V += V2
					Y += Y2
		return [Y,V]


	def add_wave (self, new_wave):
		new_wave.stop = True
		self.others_waves.append(new_wave)

	def timer(self):
		self.time += self.step

	def variables(self):
		if not  self.T == 0 and not self.l == 0:
			self.f = 1/self.T
			self.v = self.l/self.scale/self.T
			self.k = math.pi*2*self.scale/self.l
			self.w = math.pi*2/self.T
	def update(self):
		if not self.stop:
			self.clear()
			self.draw()
			self.timer()
			self.variables()

	def clear (self):
		self.panel.fill(self.panel_color)
	def draw(self):
            #-----Amplitude---#

		pygame.draw.aaline(self.panel, (255,255,255,50), (0,int(self.bottom/2-self.A/self.scale)), (self.right,int(self.bottom/2-self.A/self.scale)), True)
		pygame.draw.aaline(self.panel, (255,255,255,50), (0,int(self.bottom/2+self.A/self.scale)), (self.right,int(self.bottom/2+self.A/self.scale)), True)

            #---Text---#
		write(self.panel,'A = '+str(round(self.A,2))+' cm',(self.right+10,20))
		write(self.panel,'T = '+str(round(self.T,2))+' s',(self.right+10,40))
		write(self.panel,'V = '+str(round(self.v,2))+' m/s',(self.right+10,60))
		write(self.panel,'L = '+str(round(self.l,2))+' cm',(self.right+10,80))
		write(self.panel,'W = '+str(round(self.w,2))+' m/rad',(self.right+10,100))
		write(self.panel,'F = '+str(round(self.f,3))+' Hz',(self.right+10,120))
		write(self.panel,'Teta = '+str(round(self.teta,3))+'*PI rad',(self.right+10,140))
            #--Marcadores---#
		pygame.draw.aaline(self.panel, (255,255,255), (0,int(self.bottom/2)), (self.right,int(self.bottom/2)), True)
		pygame.draw.aaline(self.panel, (255,255,255), (0,self.bottom), (self.size[0],self.bottom), True)
		pygame.draw.aaline(self.panel, (255,255,255), (self.right,0), (self.right,self.bottom), True)
            #---focus---#
		if self.focus:
			pygame.draw.circle(self.panel,(0,255,0),(10,10),3,0)
		else:
			pygame.draw.circle(self.panel,(255,0,0),(10,10),3,0)

            #-----Draw points-----#
		last = self.points[0]
		radius = 20
		for i in range(0,self.right,10):
			pygame.draw.aaline(self.panel, (255,255,255), (i,self.bottom/2+3), (i,self.bottom/2-3), True)
		#----If is over of other wave panel----#radius
		if self.over_other_panel:
			pygame.draw.rect(self.panel, (255,255,255), (0,0,self.size[0],self.size[1]), 5)

		for x,i in enumerate(self.points):
			coor = (i[0],self.posY(i[0],self.time)[0]+ int(self.bottom/2))
			coor_y = coor[1]-self.bottom/2
			vel = self.posY(i[0],self.time)[1]
			if not last[0] == i[0]:
				self.join_points(coor,last)
			last = coor
			m = int(self.size[0]/2)
			my = self.bottom+(self.size[1]-self.bottom)/2
			if i[0] == m:
				pygame.draw.circle(self.panel, (255,0,25,100), (m, coor[1]), radius, 0)
				if not vel == 0:
					pygame.draw.line(self.panel, (255,255,255,100), (m,my), (m+vel,my), radius-1)
				if not coor_y == 0:
					pygame.draw.line(self.panel, (255,255,255,100), (m,my+radius), (m+coor_y,my+radius), radius-1)
		pygame.draw.rect(self.panel, (255,255,255), (0,my-radius/2,self.size[0],radius), 1)
		pygame.draw.rect(self.panel, (255,255,255), (0,my-radius/2+radius,self.size[0],radius), 1)
                #self.panel.set_at(coor,(255,255,255))

        #----Draw Main Lines-----#
