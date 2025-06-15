import sys

import pygame

class ship_domain:
    def __init__(self):
        pygame.init()
        title = 'double_hallship_v1'
        pygame.display.set_caption(title)
        # img = pygame.image.load('./ship.png')
        # pygame.display.set_icon(img)
        #宽**高
        self.screen = pygame.display.set_mode((1200,800))

    def draw_grid(self,rho,screen):
        a = screen.get_width()
        b=screen.get_height()
        # p=screen.get_size()
        # a=p[0]
        # b= p[1]
        range0=100*rho
        n_b=int(b/range0)+2
        n_a=int(a/range0)+2
        for j in range(n_b):
            pygame.draw.line(self.screen , 'lightgray' , (0 , range0 * j) , (a, range0 * j))
        for i in range(n_a):
            pygame.draw.line(self.screen , 'lightgray', (range0 * i , 0) , (range0 * i , b))

    def evt_lis(self,f1,f2):
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    f2 = f2+2
                elif e.key == pygame.K_DOWN:
                    f2= f2-2
                if e.key == pygame.K_w:
                    f1 = f1 + 2
                if e.key == pygame.K_s:
                    f1 = f1 - 2

            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        print(f1,f2)
        if f1>40:
            f1=40
        if f2>40:
            f2=40
        return f1,f2
from Hull_draw import *
from model import *
from collections import deque
if __name__ == '__main__':
    newship = ship_domain()
    screen = newship.screen
    rho=1.5
    r0, dt=0,0.02
    f1, f2=10,10
    x0, y0, course0, rudder, shipname, o_s=0,100,(0*np.pi/180),0,'os',[-500,-500]
    u0=0

    q = deque(maxlen=160)
    i=0
    while True:
        screen.fill('white')
        if i%100==0:
            print(i)
            q.append([x0,y0])

        x0, y0, u0, course0, r0=get_xy(x0, y0, f1, f2, u0, course0, r0, dt)
        draw_catamaran(screen, x0, y0, course0,  shipname, o_s, rho)
        newship.draw_grid(rho,screen)
        f1, f2=newship.evt_lis(f1, f2)

        draw_point(screen, q, o_s, rho)
        i += 1

        pygame.display.flip()

