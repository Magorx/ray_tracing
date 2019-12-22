from PIL import Image
from time import time

from vector import Vector
import ray_tracer


def main():
    frame_count = 1
    width = 50
    height = width
    screen_distance = width * 2
    depth = 5

    m = screen_distance

    resolution_coef = 25
    min_frame_width = 4000
    min_frame_height = 4000

    to_show = True
    to_complete_loop = False
    verbose = 1

    render_start_time = time()
    frame_start_time = 0

    camera = ray_tracer.Camera(Vector(-m / 2, 0, 0), Vector(1, 0, 0), screen_distance, width, height, resolution_coef)

    right = 90
    left = -90
    up = 75
    down = -65
    back = 240

    properties = [
        ray_tracer.Properties(Vector(0.3, 0.6, 0.3)),  # right
        ray_tracer.Properties(Vector(0.6, 0.3, 0.3)),  # left
        ray_tracer.Properties(Vector(0.4, 0.3, 0.3)),  # up
        ray_tracer.Properties(Vector(0.4, 0.3, 0.3)),  # down
        ray_tracer.Properties(Vector(0.4, 0.3, 0.3)),  # back

        ray_tracer.Properties(Vector(0.83, 0.68, 0.21), 0.2),
        ray_tracer.Properties(Vector(0, 0, 0), reflective=1),
        ray_tracer.Properties(Vector(0, 0, 0), reflective=1),
        ray_tracer.Properties(Vector(1, 0.5, 0.5), 0, 0.8, 1.75)
    ]

    r1 = 15
    r2 = 25
    r3 = 20

    objects = [
        ray_tracer.Plane(Vector(0, 0, right), Vector(0, 0, -1), properties[0]),  # right
        ray_tracer.Plane(Vector(0, 0, left), Vector(0, 0, 1), properties[1]),  # left
        ray_tracer.Plane(Vector(0, up, 0), Vector(0, -1, 0), properties[2]),  # up
        ray_tracer.Plane(Vector(0, down, 0), Vector(0, 1, 0), properties[3]),  # down
        ray_tracer.Plane(Vector(back, 0, 0), Vector(-1, 0, 0), properties[4]),  # back

        ray_tracer.Sphere(Vector(0.6 * back, down + r1, right / 3), r1, properties[5]),
        ray_tracer.Sphere(Vector(0.7 * back, down + r2, left + 1.5 * r2), r2, properties[6]),
        ray_tracer.Plane(Vector(back - 30, up - 30, right - 30), Vector(-1, -1.5, -1), properties[7]),
        ray_tracer.Sphere(Vector(0.45 * back - 5, down + 1 + 30 * 2 - 10, 3), r3, properties[8])
    ]

    pi = 3.141569
    model = ray_tracer.Model(Vector(0.45 * back - 5, down + 1, 3), 30, ray_tracer.Properties(Vector(0.3, 0.3, 1), 0.1, 0.9, 1.3, rotation=(0, 0.7, 0)), file='model.txt')
    triags = model.get_triangles()
    objects += triags

    lights = []
    coef = 900000
    lights.append(ray_tracer.Light(Vector(-100, up / 2, right / 2), Vector(1, 1, 1), distance_coef=coef*1.2))

    lights.append(ray_tracer.Light(Vector(back - 40, 0, left + 50), Vector(1, 1, 1), distance_coef=coef / 15))
    objects.append(ray_tracer.Sphere(lights[-1].o, 5, ray_tracer.Properties(Vector(1, 1, 1), 0, 0.5, 1, constant_color=True)))

    frames = []
    for frame_index in range(0, frame_count):
        # k = frame_index
        if verbose:
            frame_start_time = time()
            print('Frame_{} started'.format(frame_index))

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
