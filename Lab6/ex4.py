class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary

    def display_info(self):
        print(f"Employee ID: {self.employee_id}, Name: {self.name}, Salary: ${self.salary}")




class Manager(Employee):
    def __init__(self, name, employee_id, salary, team_size):
        super().__init__(name, employee_id, salary)
        self.team_size = team_size

    def conduct_meeting(self):
        print(f"{self.name} is conducting a meeting with the team.")

    def approve_leave(self, employee_name):
        print(f"{self.name} has approved leave for {employee_name}.")

    def display_info(self):
        super().display_info()
        print(f"Role: Manager, Team Size: {self.team_size}")


class Engineer(Employee):
    def __init__(self, name, employee_id, salary, specialty):
        super().__init__(name, employee_id, salary)
        self.specialty = specialty

    def write_code(self):
        print(f"{self.name} is writing {self.specialty} code.")

    def display_info(self):
        super().display_info()
        print(f"Role: Engineer, Specialty: {self.specialty}")


class Salesperson(Employee):
    def __init__(self, name, employee_id, salary, commission_rate):
        super().__init__(name, employee_id, salary)
        self.commission_rate = commission_rate
        self.sales_made = 0

    def make_sale(self, amount):
        self.sales_made += amount
        commission = amount * self.commission_rate
        print(f"{self.name} made a sale of ${amount}. Commission earned: ${commission}")

    def calculate_commission(self):
        total_commission = self.sales_made * self.commission_rate
        print(f"{self.name}'s total commission is ${total_commission}")
        return total_commission

    def display_info(self):
        super().display_info()
        print(f"Role: Salesperson, Commission Rate: {self.commission_rate}")



print("=== Manager Example ===")
manager = Manager(name="Alice Johnson", employee_id=101, salary=90000, team_size=10)
manager.display_info()
manager.conduct_meeting()
manager.approve_leave("Bob Smith")
print()

print("=== Engineer Example ===")
engineer = Engineer(name="Bob Smith", employee_id=102, salary=80000, specialty="Python")
engineer.display_info()
engineer.write_code()
print()

print("=== Salesperson Example ===")
salesperson = Salesperson(name="Carol Williams", employee_id=103, salary=50000, commission_rate=0.05)
salesperson.display_info()
salesperson.make_sale(2000)
salesperson.make_sale(3000)
salesperson.calculate_commission()
print()

