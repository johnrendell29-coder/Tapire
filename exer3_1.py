# User class represents a normal user
class User:
    def __init__(self, first_name, last_name):
        # Basic user information
        self.first_name = first_name
        self.last_name = last_name

    def describe_user(self):
        print(f"User: {self.first_name} {self.last_name}")


# Admin class inherits from User (meaning Admin is a special type of User)
class Admin(User):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)   # Call parent class constructor
        # Admin has a list of privileges
        self.privileges = [
            "can add user",
            "can delete user",
            "can ban user"
        ]

    # Method to show admin privileges
    def show_privileges(self):
        print("Admin privileges:")
        for privilege in self.privileges:
            print("-", privilege)


# Example usage
admin = Admin("Ren", "Taps")
admin.describe_user()
admin.show_privileges()


