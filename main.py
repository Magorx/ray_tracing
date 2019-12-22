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
    
    resolution_coef = 4
    min_frame_width = 4000
    min_frame_height = 4000

    to_show = True
    to_complete_loop = False
    verbose = 1
    
    render_start_time = time()
    frame_start_time = 0

    objects = [ray_tracer.Sphere(Vector(2 * m, 0.5 * m, 0.5 * m), radius, Vector(clr, clr, 0)),
               ray_tracer.Sphere(Vector(2 * m, 0, -0.5 * m), radius, Vector(0, clr, clr)),
               ray_tracer.Sphere(Vector(2 * m, -0.5 * m, -0.5 * m), radius, Vector(0.4, 0.2, 0.2), reflective=0.2)]

    box = ray_tracer.generate_box_for_spheres(objects, indents=[0, 0, 0, -10, 0, 0])
    for dr in box:
        if dr == 'front':
            continue
        plane = box[dr]
        r = random.uniform(0.25, 0.75)
        g = random.uniform(0.25, 0.75)
        b = random.uniform(0.25, 0.75)
        objects.append(ray_tracer.Plane(plane['p'], plane['n'], Vector(r, g, b)))

    # model = ray_tracer.Model(Vector(2 * m, +15, 0), m, color=Vector(0.7, 0.4, 0.1), file='model.txt')
    # triags = model.get_triangles()
    # objects += triags
    
    frames = []
    for frame_index in range(0, frame_count):
        # k = frame_index
        if verbose:
            frame_start_time = time()
            print('Frame_{} started'.format(frame_index))

        camera = ray_tracer.Camera(Vector(-m/2, 0, 0), Vector(1, 0, 0), screen_distance, width, height, resolution_coef)
        
        lights = []
        coef = 410000
        lights.append(ray_tracer.Light(Vector(m/2.6, 10, 10), Vector(1, 1, 1), distance_coef=coef))
    
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
