class User:
    def __init__(self, first_name, last_name, age, email, location):
        self.first_name = first_name
        self.last_name  = last_name
        self.age        = age
        self.email      = email
        self.location   = location
        self.login_attempts = 0   # NEW ATTRIBUTE

    def describe_user(self):
        print(f"\nUser Profile:")
        print(f" Name: {self.first_name} {self.last_name}")
        print(f" Age: {self.age}")
        print(f" Email: {self.email}")
        print(f" Location: {self.location}")
        print(f" Login Attempts: {self.login_attempts}")

    def greet_user(self):
        print(f"Hello, {self.first_name}! Welcome back.\n")

    # --- NEW METHODS ---
    def increment_login_attempts(self):
        self.login_attempts += 1

    def reset_login_attempts(self):
        self.login_attempts = 0


# --- TESTING THE NEW FEATURES ---

user_test = User("Ren", "Taps", 21, "ren@example.com", "Philippines")

# Simulate several login attempts
user_test.increment_login_attempts()
user_test.increment_login_attempts()
user_test.increment_login_attempts()

print(f"Login attempts after increments: {user_test.login_attempts}")

# Reset attempts
user_test.reset_login_attempts()

print(f"Login attempts after reset: {user_test.login_attempts}")
