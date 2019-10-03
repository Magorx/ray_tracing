import pygame
from time import sleep
from math import pi

from vector import *
import ray_tracer as RT


def main():
    width = 23
    height = width
    res_coef = 1
    min_frame_width = 500
    min_frame_height = 500    

    pygame.init()
    pygame.display.set_caption("AACERRRTY")
    screen = pygame.display.set_mode((min_frame_width, min_frame_height))
    pygame.display.flip()    
    
    distance = width * 2
    head = Vector(0, 1, 0)
    direction = Vector(1, 0, 0)
    
    
    # magic constants
    a = 10
    r = a / 3
    # magic constants end
    
    camera = RT.Camera(head, direction, distance, width, height, res_coef)
    objects = []
    objects.append(RT.Sphere(Vector(2 * a, 0, 0), r, Vector(0.7, 1, 0.7), 0, 0))
    objects.append(RT.Sphere(Vector(2 * a, a / 1.3, 0), r, Vector(0.5, 0.2, 0.4), 0, 0))
    objects.append(RT.Sphere(Vector(a, 0, -2 * a), r, Vector(0.9, 0.6, 0.1), 0, 0))
    objects.append(RT.Sphere(Vector(a, 0, 2 * a), r, Vector(0.1, 0.3, 0.9), 0, 0))
    objects.append(RT.Plane(Vector(0, 0, 0), Vector(0, 1, 0), Vector(0.8, 0.8, 0.8), 0, type=RT.SQUARED, scale=0.2))
    lights = []
    lights.append(RT.Light(Vector(0, 100, 100), Vector(1, 1, 1), distance_coef=sqrt(2) * 200000))
    scene = RT.Scene(camera, objects, lights)
    
    keys = set()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit() 
                exit()
            if event.type == pygame.KEYDOWN:
                keys.add(chr(event.key))
            if event.type == pygame.KEYUP:
                keys.remove(chr(event.key))

        for k in keys:
            if k == 'w':
                scene.camera.o += camera.d
            elif k == 'a':
                camera.d = roty(camera.d, pi/100)
                print(camera.d)
            elif k == 's':
                scene.camera.o -= camera.d
            elif k == 'd':
                camera.d = roty(camera.d, -pi/100)
            elif k == 'q':
                camera.d = roty(camera.d, pi/30) 
            elif k == 'e':
                camera.d = roty(camera.d, -pi/30)                 
        scene.camera.update()

        frame = RT.render_image(scene=scene, verbose=0, pygame_mode=True)
        frame = pygame.transform.scale(frame, (min_frame_width, min_frame_height))
        #frame.save('screen.png')
        screen.blit(frame, (0, 0))
        
        pygame.display.flip() 
        #sleep(1/30)


if __name__ == '__main__':
    main()