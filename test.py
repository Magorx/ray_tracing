from math import sqrt
from PIL import Image


AMBIENT = 0.1


class Vector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return (self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def len(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normal(self):
        l = self.len()
        return Vector(self.x / l, self.y / l, self.z / l)

    def proection(self, other):
        return self.normal() * self.dot(other.normal()) * other.len()
    
    def to_ints(self):
        return Vector(int(self.x), int(self.y), int(self.z))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        assert type(other) == float or type(other) == int
        return Vector(self.x * other, self.y * other, self.z * other)

    def __pow__(self, other):
        return Vector(self.x ** other, self.y ** other, self.z ** other)

    def __repr__(self):
        return '{' + '{}, {}, {}'.format(self.x, self.y, self.z) + '}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z


class Ray:
    def __init__(self, origin, direction):
        self.o = origin
        self.d = direction
    
    def __repr__(self):
        return self.d.__repr__()


class Sphere:
    def __init__(self, center, radius, color, reflective):
        self.c = center
        self.r = radius
        self.color = color
        self.reflective = reflective
    
    def intersect(self, ray):
        c_o = ray.o - self.c
        q = self.r ** 2 - (c_o.dot(c_o) - ray.d.dot(c_o) ** 2)
        if q < 0:
            return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
        else:
            d = -ray.d.dot(c_o)
            d1 = d - sqrt(q)
            d2 = d + sqrt(q)
            
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
    def __init__(self, point, normal, color, reflective):
        self.p = point
        self.n = normal
        self.color = color
        self.reflective = reflective
    
    def intersect(self, ray):
        d = self.n.dot(ray.d)
        if abs(d) < 0.000001:
            return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
        else:
            d = (self.p - ray.o).dot(self.n) / d
            if d < 0:
                return Intersection(Vector(0, 0, 0), -1, Vector(0, 0, 0), self)
            else:
                return Intersection(ray.o + ray.d * d, d, self.n, self)


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


class Camera:
    def __init__(self, origin, direction, width, height, res_x, res_y):
        self.o = origin
        self.d = direction
        self.w = width
        self.h = height
        self.res_x = res_x
        self.res_y = res_y
        
        self.left_upper = self.d + Vector(0, width/2, -height/2)
    
    def get_ray(self, x, y):
        return Ray(self.o, (self.left_upper + Vector(0, -x * self.w / self.res_x, y * self.h / self.res_y)).normal())


class Light:
    def __init__(self, origin, color):
        self.o = origin
        self.color = color


def test_ray(ray, objects, to_ignore=None):
    intersect = Intersection(Vector(0,0,0), -1, Vector(0,0,0), None)
    for obj in objects:
        if obj is to_ignore:
            continue
        cur = obj.intersect(ray)
        if cur.d > 0 and intersect.d < 0:
            intersect = cur
        elif 0 < cur.d and cur.d < intersect.d:
            intersect = cur
    return intersect


def mix(a, b, mix):
    return b * mix + a * (1 - mix)


def trace(ray, objects, lights, depth=1):
    if not depth:
        return (AMBIENT, AMBIENT, AMBIENT)
    intersection = test_ray(ray, objects)
    if intersection.d == -1:
        return (AMBIENT, AMBIENT, AMBIENT)
    else:
        color = intersection.obj.color
        if depth and intersection.obj.reflective:
            refvec = (ray.d - intersection.n * 2 * ray.d.dot(intersection.n)).normal()
            refray = Ray(intersection.p + refvec * 0.0001, refvec) # bios to prevent ray hitting itselfs origin
            refcolor = trace(refray, objects, lights, depth - 1)
            refcolor = Vector(refcolor[0], refcolor[1], refcolor[2])
            color = color + refcolor * intersection.obj.reflective
        light_effect = AMBIENT
        for light in lights:
            p_o = (light.o - intersection.p)
            d = test_ray(Ray(intersection.p + p_o.normal(), p_o.normal()), objects, intersection.obj).d
            if d != -1 and d < p_o.len():
                continue
            else:
                refl = intersection.obj.reflective
                lightIntensity = 200000.0/(4*3.1415*(light.o-intersection.p).len()**(2 - refl / 5))
                power = max(intersection.n.dot((p_o).normal() * lightIntensity), AMBIENT)
                if power != AMBIENT:
                    power = power + refl * intersection.n.dot((p_o).normal()) ** (100 * refl)
                if light_effect == AMBIENT:
                    light_effect = power
                else:
                    light_effect += power
        
        color = color * light_effect
                
    return (color.x, color.y, color.z)


def get_color(color):
    return tuple(map(lambda x: min(255, int(x * 255)), color))


BACKGROUND = Vector(AMBIENT, AMBIENT, AMBIENT)


def main():
    for k in range(0, 1):
        print('render {}'.format(k))
        m = 50
        w = m
        h = m
        res = 4
        img = Image.new('RGB', (int(w * res), int(h * res)))
        c = Camera(Vector(0, 0, 0), Vector(m, 0, 0), w, h, int(w * res), int(h * res))
        
        objects = []
        objects.append(Sphere(Vector(m + 2 * m - 14, m / 2 - 8, -4), m/3, Vector(0.3, 0.6, 0.6), 0))
        objects.append(Sphere(Vector(m + 2 * m, m / 2, 0), m / 2, Vector(1, 0, 0), 0))
        objects.append(Sphere(Vector(m + 2 * m, - m / 2, -m / 4), m / 4, Vector(0.5, 0.25, 0.125), 1))
        objects.append(Sphere(Vector(m + 2 * m, 0.2 * m, m), m / 3, Vector(0, 1, 0), 0))
        objects.append(Plane(Vector(0, - m / 2 - m / 4, 0), Vector(0, 1, 0), Vector(1, 0, 0), 0))
        objects.append(Plane(Vector(4 * m + m / 3, 0, 0), Vector(-1, 0, 0), Vector(0, 1, 1), 0))
        #objects.append(Plane(Vector(0, m / 2 + m / 3 + 20, 0), Vector(0, -1, 0), Vector(1, 1, 1), 0))
        
        #objects = [Sphere(Vector(m, 0, 0), m / 4, Vector(0.3, 0.6, 0.6), 0), Sphere(Vector(m * 0.75, 0, -m * 0.15), m / 8, Vector(0.7, 0.2, 0.8), 0)]
        #d = objects[0].c - objects[1].c
        #objects[1].c += d * (0.05 * 10) - d * (0.05 * (k - 10))
        lights = []
        lights.append(Light(Vector(20, -5, -m - 15), Vector(1, 1, 1)))
        
        for y in range(c.res_y):
            if y % (c.res_y // (10)) == 0:
                print(y / (c.res_y))
            for x in range(c.res_x):
                ray = c.get_ray(y, x)
                color = trace(ray, objects, lights, depth=2)
                img.putpixel((x, y), get_color(color))
        size = max(500, m * res)
        img = img.resize((size, size), Image.NEAREST)
        img.save('render{}.png'.format(k))

main()