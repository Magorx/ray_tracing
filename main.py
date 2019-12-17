from math import sqrt, sin, cos
from PIL import Image
from time import time

from vector import Vector
import ray_tracer
import random


def main():
    frame_count = 1
    width = 50
    height = width
    screen_distance = width * 2
    depth = 4
    
    m = screen_distance
    radius = m / 4
    clr = 0.75    
    
    resolution_coef = 16
    min_frame_width = 4000
    min_frame_height = 4000

    to_show = True
    to_complete_loop = False
    verbose = 1
    
    render_start_time = time()
    '''
    objects.append(ray_tracer.Sphere(Vector(2 * m, 0.5 * m, 0.5 * m), radius, Vector(clr, clr, 0)))
    objects.append(ray_tracer.Sphere(Vector(2 * m, 0, -0.5 * m), radius, Vector(0, clr, clr)))
    objects.append(ray_tracer.Sphere(Vector(2 * m, -0.5 * m, -0.5 * m), radius, Vector(0.4, 0.2, 0.2), reflective=0.2))
    #objects.append(ray_tracer.Sphere(Vector(1.5 * m, -radius, -0.25 * m), radius, Vector(0.4, 0.7, 0.5), 0, 1.075, 1))
    
    box = ray_tracer.generate_box_for_spheres(objects, indent=0)
    for dr in box:
        plane = box[dr]
        r = random.uniform(0.25, 0.75)
        g = random.uniform(0.25, 0.75)
        b = random.uniform(0.25, 0.75)
        objects.append(ray_tracer.Plane(plane['p'], plane['n'], Vector(r, g, b)))
    objects.append(ray_tracer.Sphere(Vector(box['back']['p'].x, box['down']['p'].y, box['right']['p'].z), 2.5 * radius, Vector(0, clr/3, clr), 0.2, 0))
    
    model = ray_tracer.Model(Vector(2 * m + radius, 0, 0), m, color=Vector(0.7, 0.4, 0.1), reflective=0.05, file='model.txt')
    objects += model.get_triangles()
    '''
    
    frames = []
    for frame_index in range(0, frame_count):
        k = frame_index
        if verbose:
            frame_start_time = time()
            print('Frame_{} started'.format(frame_index))

        camera = ray_tracer.Camera(Vector(-m/2.5, 0, 0), Vector(1, 0, 0), screen_distance, width, height, resolution_coef)
        
        objects = []
        bias = Vector(-m/5*3, 0, 0)
        objects.append(ray_tracer.Sphere(Vector(m, 0, 0) + bias, radius, Vector(clr, clr, 0)))        

        #p1 = objects[1].c + Vector(-0.5 * m, 0, 0)
        #p2 = objects[2].c + Vector(-m, 0, 0)
        #p3 = objects[0].c + Vector(0, 0, 0)
        #objects.append(ray_tracer.Triangle(p1, p2, p3, Vector(0.7, 0.4, 0.1), refractive_coef=0.7, refractive=1))
        
        #objects.append(ray_tracer.Plane(Vector(0, -0.1 * m, 0), Vector(0, 1, 0), Vector(0, 0, 0), refractive_coef=1.4, refractive=1))
        
        lights = []
        coef = 30000 #410000
        lights.append(ray_tracer.Light(Vector(m/3, 0, 0) + bias, Vector(1, 1, 1), distance_coef=coef))     
        #lights.append(ray_tracer.Light(Vector(m/2.6, 10, 0), Vector(1, 1, 1), distance_coef=coef))     
    
        frame = ray_tracer.render_image(camera, objects, lights, depth, verbose)
        if camera.res_x < min_frame_width or camera.res_y < min_frame_height:
            frame = frame.resize((min_frame_width, min_frame_height), Image.NEAREST)
        
        if to_show:
            frame.show()
        if verbose:
            frame_finish_time = time()
            print('Frame_{} finished in {:.2f}'.format(frame_index, frame_finish_time - frame_start_time))
        frame.save('frame{}.png'.format(frame_index))
        if to_complete_loop:
            frame.save('frame{}.png'.format(frame_count * 2 - frame_index - 1))
    
    if to_complete_loop:
        if verbose:
            print('Completing loop')

        frames = frames + frames[-1:-len(frames) - 1:-1]
        for i in range(frame_count, len(frames)):
            frames[i].save('frame{}.png'.format(i))

    if verbose:
        render_finish_time = time()
        print('Render finished in {:.2f}'.format(render_finish_time - render_start_time))


if __name__ == '__main__':
    main()