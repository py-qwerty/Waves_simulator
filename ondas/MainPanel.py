import pygame
import subprocess
import wave
import time
pygame.init()
pygame.event.set_grab(True)
def screen_size():
    size = (None, None)
    args = ["xrandr", "-q", "-d", ":0"]
    proc = subprocess.Popen(args,stdout=subprocess.PIPE)
    for line in proc.stdout:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
            if "Screen" in line:
                size = (int(line.split()[7]),  int(line.split()[9][:-1]))
    return size

def colision_rect (pos1,size1,pos2,size2):
    if pos1[0]+size1[0] > pos2[0] and pos1[0] < pos2[0] + size2[0] and pos1[1]+size1[1] > pos2[1] and pos1[1] < pos2[1] + size2[1]:
        return True
    else:
        return False

class MainPanel:
        def  __init__(self):
                #-----Variables
                self.second_penels = list()
                self.taken_panel = None
                self.colWaves = list()
                self.size = screen_size()
                self.panel = pygame.Surface(self.size).convert_alpha()
                self.panel.fill((0,0,0))
                self.relative_mouse_position = list()
                self.focus_panel = None
                self.first_pressed = ()
                self.pressed = False
                self.one_enought = None
                self.new = True
                self.keytime = 0

        def Key_control (self):
            self.keytime +=1
            if self.keytime == 3:
                self.keytime =0
                k = pygame.key.get_pressed()
                if k[pygame.K_t]:
                    if k[pygame.K_UP]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                                self.focus_panel.T += 5
                if k[pygame.K_l]:
                    if k[pygame.K_UP]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                                self.focus_panel.l += 1

                if k[pygame.K_s]:
                    if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                        self.focus_panel.dir *=-1

                if k[pygame.K_a]:
                    if k[pygame.K_UP]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                                self.focus_panel.A += 0.1

                if k[pygame.K_o]:
                    if k[pygame.K_UP]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                                self.focus_panel.teta += 0.6
                #-----Down-----#
                if k[pygame.K_DOWN]:
                    if k[pygame.K_t]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                            self.focus_panel.T -= 5

                    if k[pygame.K_l]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                            self.focus_panel.l -= 1

                    if k[pygame.K_a]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                            self.focus_panel.A -= 0.1

                    if k[pygame.K_o]:
                        if not self.focus_panel == None and self.focus_panel.type == 'Wave':
                            self.focus_panel.teta -= 0.1
                #--Crate New Wave_Panel---#
                if k[pygame.K_LCTRL] and self.new:
                    self.new = False
                    if k[pygame.K_n]:
                        Wave = wave.Wave(5,100,10)
                        self.add_wave(Wave)
                    if k[pygame.K_e]:
                        Wave = wave.Wave(5,100,10)
                        Wave2 = wave.Wave(5,100,10,0.5,-1)
                        Wave.add_wave(Wave2)
                        self.add_wave(Wave)
                    if k[pygame.K_r]:
                        Wave = wave.Wave(5,100,66)
                        Wave2 = wave.Wave(5,100,66,0,-1)
                        Wave.add_wave(Wave2)
                        self.add_wave(Wave)
                    if k[pygame.K_f]:
                        Wave = wave.Wave(5,100,50)
                        Wave2 = wave.Wave(5,100,50,0,-1)
                        Wave.add_wave(Wave2)
                        self.add_wave(Wave)

                    if k[pygame.K_d]:
                        self.delate_waves()
                else:
                    self.new = True

        def delate_waves(self):
            self.second_penels = list()
            self.taken_panel = None
        def Mouse_control(self):
            mouse = pygame.mouse
            kx = 0
            ky = 0
            self.pressed = mouse.get_pressed()[0]
            if mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if not len(self.first_pressed):
                    self.first_pressed = pos
                if not self.taken_panel == None:
                    if not len(self.relative_mouse_position):
                        self.relative_mouse_position.append(pos)
                        self.relative_mouse_position.append(self.taken_panel.position)
                    kx = self.relative_mouse_position[0][0]-self.relative_mouse_position[1][0]
                    ky = self.relative_mouse_position[0][1]-self.relative_mouse_position[1][1]

                    p = self.taken_panel.position
                    self.taken_panel.position = (pos[0]-kx,pos[1]-ky)
            else:
                if not self.taken_panel == None and not self.taken_panel.over_other_panel:
                    self.taken_panel = None
                self.relative_mouse_position = list()
                self.first_pressed = ()

        def add_wave(self, wave):
            self.second_penels.append(wave)

        def update(self):
            self.Key_control()
            self.clean_Surface()
            self.Mouse_control()
            self.update_second_penels()



        def clean_Surface (self):
                self.panel.fill((10,10,10))

        def update_second_penels(self):

            pos  = pygame.mouse.get_pos()
            if not self.taken_panel == None:
                self.panel.blit(self.taken_panel.panel,self.taken_panel.position)

            for i in self.second_penels:
                    i.update()
                    self.panel.blit(i.panel,i.position)
                    if not self.taken_panel == None and not i == self.taken_panel:
                        i.focus = False
                        #----Comprovamos que esta sore otra wave----#
                        if colision_rect(self.taken_panel.position,self.taken_panel.size,i.position,i.size):
                            self.one_enought = i
                            self.taken_panel.over_other_panel = True
                            if not self.pressed:
                                #-----Diferenciamos entre los tipos de paneles y el tipo de intereccion entre ellos----#
                                if self.taken_panel.type == 'Wave':
                                    if i.type == 'Wave':
                                        i.others_waves.append(self.taken_panel)
                                    if i.type == 'ColWave':
                                        pass

                                    self.second_penels.remove(self.taken_panel)
                                    self.taken_panel = None

                        else:
                            if self.one_enought == i:
                                self.taken_panel.over_other_panel = False




                    if len(self.first_pressed):
                            if colision_rect(self.first_pressed,(0,0),i.position,i.size):
                                if not i == self.taken_panel and self.taken_panel == None:
                                    self.taken_panel = i
                                    self.focus_panel = i
                                    self.taken_panel.focus = True
