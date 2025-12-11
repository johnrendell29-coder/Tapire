# Privileges class handles ONLY privileges
class Privileges:
    def __init__(self, privileges=None):
        # If no privileges are passed, create an empty list
        if privileges is None:
            privileges = []

        # Use a "private-like" variable (convention)
        self._privileges = privileges

    # Getter method → returns the privileges list
    def get_privileges(self):
        return self._privileges

    # Setter method → updates the privileges list
    def set_privileges(self, privileges):
        self._privileges = privileges

    # Show privileges
    def show_privileges(self):
        print("Admin privileges:")
        for privilege in self._privileges:
            print("-", privilege)


# Admin class now uses a Privileges object
class Admin:
    def __init__(self, name):
        self.name = name

        # Admin has its own Privileges instance
        self.privileges = Privileges()


# Example usage
admin1 = Admin("Ren")

# Set privileges using setter
admin1.privileges.set_privileges([
    "can add user",
    "can delete user",
    "can ban user"
])

# Show privileges
admin1.privileges.show_privileges()

