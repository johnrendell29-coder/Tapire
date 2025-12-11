# This is the User class from Programming Exercise 2
class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.login_attempts = 0  # default value

    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0


# Admin is a special kind of User → so we inherit from User
class Admin(User):
    def __init__(self, first_name, last_name):
        super().__init__(first_name, last_name)  
        # super() lets Admin use User’s __init__

        # list of privileges for admins
        self.privileges = [
            "can add post",
            "can delete post",
            "can ban user",
            "can reset password"
        ]

    # prints all privileges
    def show_privileges(self):
        print("Admin privileges:")
        for privilege in self.privileges:
            print("-", privilege)


# Create an admin user
admin_user = Admin("Rendell", "Tapire")

# Call the method
admin_user.show_privileges()
