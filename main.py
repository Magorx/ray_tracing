from math import sqrt
from PIL import Image
from time import time

from vector import Vector


AMBIENT = 0.1
BACKGROUND = Vector(AMBIENT, AMBIENT, AMBIENT)
MAG = 1
ANDY = 2
DISTANT = 3


class Ray:
    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction
    
    def __repr__(self):
        return self.d.__repr__()


class Sphere:
    def __init__(self, center, radius, color, reflective=0, refractive=0):
        self.c = center
        self.r = radius
        self.color = color
        self.reflective = reflective
        self.refractive = refractive
    
    def intersect(self, ray):
        c_o = ray.o - self.c
        discriminant = self.r ** 2 - (c_o.dot(c_o) - ray.d.dot(c_o) ** 2)
        if discriminant < 0:
            return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
        else:
            b = -ray.d.dot(c_o)
            d1 = b - sqrt(discriminant)
            d2 = b + sqrt(discriminant)
            
            if d1 > 0 and (d2 > d1 or d2 < 0):
                d = d1
            elif d2 > 0 and (d1 > d2 or d1 < 0):
                d = d2
            else:
                return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
            
            point = ray.o + ray.d * d
            return Intersection(point, d, self.normal(point), self)
    
    def normal(self, other):
        return (other - self.c).normal()


class Plane:
    def __init__(self, point, normal, color, reflective=0, refractive=0):
        self.p = point
        self.n = normal
        self.color = color
        self.reflective = reflective
        self.refractive = refractive
    
    def intersect(self, ray):
        cos = self.n.dot(ray.d)
        if abs(cos) < 0.000001:
            return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
        else:
            cos = (self.p - ray.o).dot(self.n) / cos
            if cos < 0:
                return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
            else:
                return Intersection(ray.o + ray.d * cos, cos, self.n, self)


class Intersection:
    def __init__(self, point, distance, normal, obj):
        self.p = point
        self.d = distance
        self.n = normal
        self.obj = obj
    
    def __eq__(self, other):
        return self.p == other.p and self.d == other.d and self.n == other.n and self.obj == other.obj
    
    def __repr__(self):
        return 'Intersection<p[{}], d[{}]>'.format(self.p, self.d)


class Light:
    def __init__(self, origin, color, type=MAG, distance_coef=200000):
        self.o = origin
        self.color = color
        self.type = type
        self.distance_coef = distance_coef
    
    def calculate_effect(self, point, normal, obj, objects):
        if self.type == MAG:
            p_o = self.o - point
            if p_o.len() == 0:
                return self.color
            
            intersection = test_ray(Ray(point + p_o.normal(), p_o.normal()), objects, [obj])
            dist = intersection.d            
            if dist != -1 and dist < p_o.len() and not intersection.obj.refractive:
                return Vector(0, 0, 0)
            else:
                reflection_coef = obj.reflective
                intensity = self.distance_coef / (12.5 * p_o.len() ** (2 - reflection_coef / 5))
                power = max(normal.dot((p_o).normal() * intensity), AMBIENT)
                if power != AMBIENT:
                    power = power + reflection_coef * normal.dot((p_o).normal()) ** (100 * reflection_coef)
                return self.color * power

        elif self.type == DISTANT:
            p_o = self.o.normal() * -1
            intersection = test_ray(Ray(point + p_o * 0.0001, p_o), objects, obj)
            if intersection.d != -1:
                return Vector(0, 0, 0)
            else:
                return self.color * (-self.o.dot(normal))

class Camera:
    def __init__(self, origin, direction, width, height, res_x, res_y):
        self.o = origin
        self.d = direction
        self.w = width
        self.h = height
        self.res_x = res_x
        self.res_y = res_y
        
        self.left_upper = self.d + Vector(0, width/2, -height / 2)
    
    def get_ray(self, x, y):
        return Ray(self.o, (self.left_upper + Vector(0, -x * self.w / self.res_x, y * self.h / self.res_y)).normal())


def test_ray(ray, objects, to_ignore=[]):
    intersection = Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), None)
    for obj in objects:
        if obj in to_ignore:
            continue
        current_intersection = obj.intersect(ray)
        if current_intersection.d > 0 and intersection.d < 0:
            intersection = current_intersection
        elif 0 < current_intersection.d and current_intersection.d < intersection.d:
            intersection = current_intersection
    return intersection


def get_color(color):
    return tuple(map(lambda x: min(255, int(x * 255)), [color.x, color.y, color.z]))


def trace(ray, objects, lights, depth=1):
    if not depth:
        return BACKGROUND
    intersection = test_ray(ray, objects)
    if intersection.d == -1:
        return BACKGROUND
    
    obj = intersection.obj
    color = obj.color
    
    light_effect = Vector(0, 0, 0)
    for light in lights:
        light_effect += light.calculate_effect(intersection.p, intersection.n, obj, objects)
    color = color * light_effect
    
    if depth and obj.reflective:
        reflected_vector = (ray.d - intersection.n * 2 * ray.d.dot(intersection.n)).normal()
        reflectaed_ray = Ray(intersection.p + reflected_vector * 0.0001, reflected_vector) # bios to prevent ray hitting itselfs origin
        reflected_color = trace(reflectaed_ray, objects, lights, depth - 1)
        color = color + reflected_color * intersection.obj.reflective

    if depth and obj.refractive:
        normal = intersection.n
        cos = ray.d.dot(normal)
        
        coef_from = 1
        coef_to = obj.refractive
        if cos < 0:
            cos *= -1
        else:
            normal = normal * -1
            coef_from, coef_to = coef_to, coef_from

        ratio = coef_from / coef_to
        k = 1 - ratio * ratio * (1 - cos * cos)
        if k < 0:
            pass
        else:
            refratced_vector = ray.d * ratio + normal * (ratio * cos - sqrt(k))
            refracted_ray = Ray(intersection.p + refratced_vector * 0.0001, refratced_vector) # bios to prevent ray hitting itselfs origin
            refracted_color = trace(refracted_ray, objects, lights, depth - 1)
            color = color + refracted_color
                
    return color


def render_image(camera, objects, lights, depth, verbose=1):
    img = Image.new('RGB', (camera.res_x, camera.res_y))
    
    for y in range(camera.res_y):
        if verbose:
            if y % (camera.res_y // (10)) == 0:
                print(y / (camera.res_y))
        for x in range(camera.res_x):
            ray = camera.get_ray(y, x)
            color = trace(ray, objects, lights, depth)
            img.putpixel((x, y), get_color(color))
    
    if verbose:
        print('1.0')
    return img


def main():
    frame_count = 1
    screen_distance = 50
    width = screen_distance
    height = screen_distance
    depth = 5
    
    resolution_coef = 4
    min_frame_width = 500
    min_frame_height = 500
    
    to_show = True
    verbose = 1
    
    render_start_time = time()
    
    for frame_index in range(0, frame_count):
        if verbose:
            frame_start_time = time()
            print('Frame_{} started'.format(frame_index + 1))

        res_x = width * resolution_coef
        res_y = height * resolution_coef
        camera = Camera(Vector(0, 0, 0), Vector(screen_distance, 0, 0), width, height, res_x, res_y)
        
        m = screen_distance
        
        objects = []
        objects.append(Sphere(Vector(m + 2 * m - 40, m / 2 - 15, 20), m / 2.5, Vector(0.1, 0.1, 0.3), 0.27, 1.15)) # blue sphere
        objects.append(Sphere(Vector(m + 2 * m, m / 2, 0), m / 2, Vector(1, 0, 0), 0.05)) # red sphere
        objects.append(Sphere(Vector(m + 2 * m, - m / 2, -m / 4), m / 4, Vector(0, 0, 0), 1)) # orange-mirror sphere
        objects.append(Sphere(Vector(m + 2 * m, 0.2 * m, m), m / 2.7, Vector(0, 1, 0), 0.1)) # green sphere
        objects.append(Plane(Vector(0, - m / 2 - m / 4, 0), Vector(0, 1, 0), Vector(1, 0, 0), 0.8))
        objects.append(Plane(Vector(4 * m + m / 3, 0, 0), Vector(-1, 0, 0), Vector(0, 1, 1), 0))
        objects.append(Plane(Vector(0, m / 2 + m / 3 + 20, 0), Vector(0, -1, 0), Vector(1, 1, 1), 0))
        
        lights = []
        lights.append(Light(Vector(20, -5, - m - 15), Vector(0.9, 0.17, 0.17)))
        lights.append(Light(Vector(20, 10, + m + 15), Vector(0.17, 0.55, 0.9)))
    
        frame = render_image(camera, objects, lights, depth, verbose)
        if res_x < min_frame_width or res_y < min_frame_height:
            frame = frame.resize((min_frame_width, min_frame_height), Image.NEAREST)
        
        if to_show:
            frame.show()
        if verbose:
            frame_finish_time = time()
            print('Frame_{} finished in {:.2f}'.format(frame_index, frame_finish_time - frame_start_time))
        frame.save('frame{}.png'.format(frame_index))

    if verbose:
        render_finish_time = time()
        print('Render finished in {:.2f}'.format(render_finish_time - render_start_time))


if __name__ == '__main__':
    main()