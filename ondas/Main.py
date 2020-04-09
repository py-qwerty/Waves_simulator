import pygame
import sys
import MainPanel
import colwave
import  wave
import subprocess
pygame.init()




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



class Main():
    def __init__(self):
        self.screen = pygame.display.set_mode(screen_size(),pygame.FULLSCREEN,32)
        self.clock = pygame.time.Clock()
        self.MainPanel = MainPanel.MainPanel()
        self.FPS = 60 #Hz
        self.main_loop()

    def update(self):
        self.screen.blit(self.MainPanel.panel,(0,0))
        self.MainPanel.update()


    def main_loop(self):
        while True:
            self.screen.fill([0,0,0])
            self.update()
            pygame.display.flip()
            self.clock.tick(self.FPS)
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

Main()
