class User:
    def __init__(self, first_name, last_name, age, email, location):
        self.first_name = first_name
        self.last_name  = last_name
        self.age        = age
        self.email      = email
        self.location   = location

    def describe_user(self):
        print(f"\nUser Profile:")
        print(f" Name: {self.first_name} {self.last_name}")
        print(f" Age: {self.age}")
        print(f" Email: {self.email}")
        print(f" Location: {self.location}")

    def greet_user(self):
        print(f"Hello, {self.first_name}! Welcome back.\n")


# --- Create several user instances ---

user1 = User("Ren", "Tapire", 21, "ren@example.com", "Philippines")
user2 = User("Alex", "Mine", 19, "alex@example.com", "Singapore")
user3 = User("Mika", "Sato", 22, "mika@example.com", "Japan")

# --- Call methods for each user ---

user1.describe_user()
user1.greet_user()

user2.describe_user()
user2.greet_user()

user3.describe_user()
user3.greet_user()
