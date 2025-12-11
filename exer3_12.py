# Regular User class
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def describe_user(self):
        print(f"User: {self.first_name} {self.last_name}")

# Privileges class (separate)
# Handles privilege storage + methods
class Privileges:
    def __init__(self, privileges=None):
        # If no list is provided, use an empty list
        self._privileges = privileges if privileges else []

    # Getter → returns privileges
    def get_privileges(self):
        return self._privileges

    # Setter → updates privileges
    def set_privileges(self, privileges):
        self._privileges = privileges

    # Display privileges
    def show_privileges(self):
        print("Privileges:")
        if not self._privileges:
            print("- No privileges assigned.")
        else:
            for p in self._privileges:
                print("-", p)


# Admin class → child of User
# Has its own Privileges object
class Admin(User):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)     # Inherit user info

        # Admin has a Privileges instance
        self.privileges = Privileges()

# Example Usage
admin = Admin("Ren", "Taps")
admin.describe_user()

# Set privileges using setter
admin.privileges.set_privileges([
    "can add user",
    "can delete user",
    "can ban user",
    "can reset passwords"
])

# Show privileges
admin.privileges.show_privileges()
