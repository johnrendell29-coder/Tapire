class Privileges:
    def __init__(self, privileges=None):
        if privileges is None:
            privileges = []
        self._privileges = privileges  # private attribute

    # Getter
    def get_privileges(self):
        return self._privileges

    # Setter
    def set_privileges(self, privileges):
        self._privileges = privileges

    def show_privileges(self):
        print("Admin privileges:")
        for p in self._privileges:
            print("-", p)


class Admin:
    def __init__(self, name):
        self.name = name
        self.privileges = Privileges()  # Admin has Privileges class

# -------------------------
# Example usage
# -------------------------

admin1 = Admin("Ren")

# Set privileges
admin1.privileges.set_privileges([
    "can add user",
    "can delete user",
    "can ban user"
])

# Show privileges
admin1.privileges.show_privileges()
