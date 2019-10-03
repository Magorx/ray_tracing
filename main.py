from math import sqrt, sin, cos
from PIL import Image
from time import time

from vector import Vector
import ray_tracer


def main():
    frame_count = 1
    width = 20
    height = width
    screen_distance = width * 2
    depth = 4
    
    resolution_coef = 1
    min_frame_width = 4000
    min_frame_height = 4000
    
    to_show = True
    to_complete_loop = False
    verbose = 1
    
    render_start_time = time()
    
    frames = []
    for frame_index in range(0, frame_count):
        k = frame_index
        if verbose:
            frame_start_time = time()
            print('Frame_{} started'.format(frame_index))

        m = screen_distance
        camera = ray_tracer.Camera(Vector(-screen_distance / 3, 0, 0), Vector(1, 0, 0), screen_distance, width, height, resolution_coef)
    
        objects = []
        l = m / 2
        r = m / 3
        main = 0.7
        fair = 0.3
        sc = 1
        objects.append(ray_tracer.Sphere(Vector(2 * m, 0, 0), r, Vector(sc, sc, sc), 0, 0))
        objects.append(ray_tracer.Plane(Vector(2 * m + r, 0, 0), Vector(-1, 0, 0), Vector(main, main, main), 0.4, type=ray_tracer.SQUARED, scale=3))
    
        lights = []
        dx = 50
        h = 2 * r + dx * r / l
        coef = 100000
        lights.append(ray_tracer.Light(Vector(m/2, 0, m), Vector(0.2, 0.5, 0.5), distance_coef=coef))     
    
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