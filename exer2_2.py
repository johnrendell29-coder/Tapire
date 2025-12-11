class User:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.login_attempts = 0   # starts at 0

    # adds 1 to login_attempts
    def increment_login_attempts(self):
        self.login_attempts += 1

    # resets to 0
    def reset_login_attempts(self):
        self.login_attempts = 0


# make a user
user = User("Rendell", "Tapire")

# increase attempts
user.increment_login_attempts()
user.increment_login_attempts()
user.increment_login_attempts()

print("Login attempts:", user.login_attempts)

# reset
user.reset_login_attempts()
print("After reset:", user.login_attempts)

