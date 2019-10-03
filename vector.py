from math import sqrt, sin, cos


class Vector:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    def len(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normal(self):
        l = self.len()
        if l == 0:
            return Vector(0, 0, 0)
        else:
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
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            assert type(other) == float or type(other) == int
            return Vector(self.x * other, self.y * other, self.z * other)
    
    def __truediv__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            assert type(other) == float or type(other) == int
            return Vector(self.x / other, self.y / other, self.z / other)        

    def __pow__(self, other):
        return Vector(self.x ** other, self.y ** other, self.z ** other)

    def __repr__(self):
        return '{' + '{}, {}, {}'.format(self.x, self.y, self.z) + '}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other):
        return self.x < other.x or self.y < other.y or self.z < other.z


def rotx(vec, ang):
    x = vec.x
    y = vec.y * cos(ang) - vec.z * sin(ang)
    z = vec.y * sin(ang) + vec.z * cos(ang)
    return Vector(x, y, z)

def roty(vec, ang):
    x = vec.x * cos(ang) + vec.z * sin(ang)
    y = vec.y
    z = vec.z * cos(ang) - vec.x * sin(ang)
    return Vector(x, y, z)

def rotz(vec, ang):
    x = vec.x * cos(ang) - vec.y * sin(ang)
    y = vec.y * cos(ang) - vec.x * sin(ang)
    z = vec.z
    return Vector(x, y, z)

def rot(vec, dx, dy, dz):
    return rotz(roty(rotx(vec, dx), dy), dz)