class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def calculate_mileage(self):
        print("Mileage calculation not implemented for base Vehicle class.")
        return 0

    def calculate_towing_capacity(self):
        print("Towing capacity calculation not implemented for base Vehicle class.")
        return 0

    def display_info(self):
        print(f"{self.year} {self.make} {self.model}")


class Car(Vehicle):
    def __init__(self, make, model, year, mpg):
        super().__init__(make, model, year)
        self.mpg = mpg

    def calculate_mileage(self):
        print(f"The car's mileage is {self.mpg} MPG.")
        return self.mpg


class Motorcycle(Vehicle):
    def __init__(self, make, model, year, mpg):
        super().__init__(make, model, year)
        self.mpg = mpg

    def calculate_mileage(self):
        print(f"The motorcycle's mileage is {self.mpg} MPG.")
        return self.mpg


class Truck(Vehicle):
    def __init__(self, make, model, year, towing_capacity):
        super().__init__(make, model, year)
        self.towing_capacity = towing_capacity

    def calculate_towing_capacity(self):
        print(f"The truck's towing capacity is {self.towing_capacity} kg.")
        return self.towing_capacity



print("=== Car Example ===")
car = Car(make="Toyota", model="Camry", year=2020, mpg=28)
car.display_info()
car.calculate_mileage()
print()

print("=== Motorcycle Example ===")
motorcycle = Motorcycle(make="Harley-Davidson", model="Street 750", year=2019, mpg=55)
motorcycle.display_info()
motorcycle.calculate_mileage()
print()

print("=== Truck Example ===")
truck = Truck(make="Ford", model="F-150", year=2021, towing_capacity=13000)
truck.display_info()
truck.calculate_towing_capacity()
print()

print("=== Base Vehicle Example ===")
vehicle = Vehicle(make="Generic", model="Vehicle", year=2022)
vehicle.display_info()
vehicle.calculate_mileage()
vehicle.calculate_towing_capacity()
