class Animal:
    def __init__(self, name):
        self.name = name

    def move(self):
        print(f"{self.name} moves in its own way.")

    def make_sound(self):
        print(f"{self.name} makes a sound.")

    def display_info(self):
        print(f"Animal Name: {self.name}")


class Mammal(Animal):
    def __init__(self, name, gestation_period):
        super().__init__(name)
        self.gestation_period = gestation_period

    def feed_young(self):
        print(f"{self.name} is feeding its young with milk.")

    def display_info(self):
        super().display_info()
        print(f"Type: Mammal, Gestation Period: {self.gestation_period} days")


class Bird(Animal):
    def __init__(self, name, wing_span):
        super().__init__(name)
        self.wing_span = wing_span

    def fly(self):
        print(f"{self.name} is flying with a wingspan of {self.wing_span} meters.")

    def lay_eggs(self):
        print(f"{self.name} is laying eggs.")

    def display_info(self):
        super().display_info()
        print(f"Type: Bird, Wingspan: {self.wing_span} meters")


class Fish(Animal):
    def __init__(self, name, water_type):
        super().__init__(name)
        self.water_type = water_type  # 'freshwater' or 'saltwater'

    def swim(self):
        print(f"{self.name} is swimming in the {self.water_type}.")

    def display_info(self):
        super().display_info()
        print(f"Type: Fish, Water Type: {self.water_type}")

print("=== Mammal Example ===")
mammal = Mammal(name="Elephant", gestation_period=640)
mammal.display_info()
mammal.move()
mammal.make_sound()
mammal.feed_young()
print()

print("=== Bird Example ===")
bird = Bird(name="Eagle", wing_span=2.3)
bird.display_info()
bird.move()
bird.make_sound()
bird.fly()
bird.lay_eggs()
print()

print("=== Fish Example ===")
fish = Fish(name="Salmon", water_type="freshwater")
fish.display_info()
fish.move()
fish.make_sound()
fish.swim()
print()

print("=== Base Animal Example ===")
animal = Animal(name="Generic Animal")
animal.display_info()
animal.move()
animal.make_sound()
