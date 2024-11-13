class Account:
    def __init__(self, account_number, balance=0):
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount} into account {self.account_number}. New balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew {amount} from account {self.account_number}. New balance: {self.balance}")
        else:
            print(f"Insufficient funds in account {self.account_number}. Withdrawal failed.")

    def calculate_interest(self):
        print("Interest calculation not implemented for base Account class.")
        return 0


class SavingsAccount(Account):
    def __init__(self, account_number, balance=0, interest_rate=0.02):
        super().__init__(account_number, balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        print(f"Calculated interest for SavingsAccount {self.account_number}: {interest}")
        return interest


class CheckingAccount(Account):
    def __init__(self, account_number, balance=0, overdraft_limit=0):
        super().__init__(account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if self.balance + self.overdraft_limit >= amount:
            self.balance -= amount
            print(f"Withdrew {amount} from account {self.account_number}. New balance: {self.balance}")
        else:
            print(f"Overdraft limit reached for account {self.account_number}. Withdrawal failed.")

    def calculate_interest(self):
        print(f"Interest calculation not applicable for CheckingAccount {self.account_number}.")
        return 0


print("=== SavingsAccount Example ===")
savings_acc = SavingsAccount(account_number=1001, balance=1000, interest_rate=0.05)
savings_acc.deposit(500)
savings_acc.withdraw(200)
interest = savings_acc.calculate_interest()
savings_acc.balance += interest
print(f"New balance after adding interest: {savings_acc.balance}\n")

print("=== CheckingAccount Example ===")
checking_acc = CheckingAccount(account_number=2001, balance=500, overdraft_limit=300)
checking_acc.deposit(200)
checking_acc.withdraw(800)
checking_acc.withdraw(300)
interest = checking_acc.calculate_interest()
print(f"Balance remains: {checking_acc.balance}\n")

print("=== Base Account Example ===")
basic_acc = Account(account_number=3001, balance=100)
basic_acc.deposit(50)
basic_acc.withdraw(30)
basic_acc.calculate_interest()
print(f"Final balance for basic account: {basic_acc.balance}")
