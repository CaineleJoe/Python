import math
#ex1
class Shape:
    def area(self):
        return "Area method not implemented for base Shape class."

    def perimeter(self):
        return "Perimeter method not implemented for base Shape class."

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self):
        return self.a + self.b + self.c


circle = Circle(radius=5)
print("Circle area:", circle.area())
print("Circle perimeter:", circle.perimeter())

rectangle = Rectangle(width=4, height=6)
print("\nRectangle area:", rectangle.area())
print("Rectangle perimeter:", rectangle.perimeter())

triangle = Triangle(a=3, b=4, c=5)
print("\nTriangle area:", triangle.area())
print("Triangle perimeter:", triangle.perimeter())

shape = Shape()
print(shape.area())
print(shape.perimeter())
