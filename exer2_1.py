class User:
    # sets initial values when creating a User
    def __init__(self, first_name, last_name, age, email):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email

    # prints user information
    def describe_user(self):
        print(f"Name: {self.first_name} {self.last_name}")
        print(f"Age: {self.age}")
        print(f"Email: {self.email}")

    # prints a simple greeting
    def greet_user(self):
        print(f"Hello, {self.first_name}!")


# make some users
user1 = User("Rendell", "Tapire", 20, "rendell@example.com")
user2 = User("Llyod", "Frontera", 22, "Llyod@example.com")

user1.describe_user()
user1.greet_user()

user2.describe_user()
user2.greet_user()

