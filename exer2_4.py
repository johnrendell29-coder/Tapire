class Restaurant:
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type
        self.number_served = 0   # default value

    def describe_restaurant(self):
        print(f"Restaurant Name: {self.restaurant_name}")
        print(f"Cuisine Type: {self.cuisine_type}")

    def open_restaurant(self):
        print(f"{self.restaurant_name} is now open!")

    def set_number_served(self, number):
        self.number_served = number

    def increment_number_served(self, amount):
        self.number_served += amount


# Create instance
restaurant = Restaurant("Special GOTO ni Rendell", "Filipino Cuisine")

# Print initial number served
print("Number served:", restaurant.number_served)

# Change the value and print again
restaurant.number_served = 15
print("Number served after manual change:", restaurant.number_served)

# Set new number using method
restaurant.set_number_served(50)
print("Number served after set_number_served:", restaurant.number_served)

# Increment number served
restaurant.increment_number_served(30)
print("Number served after increment:", restaurant.number_served)
