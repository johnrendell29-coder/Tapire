class Restaurant:
    # sets starting values
    def __init__(self, restaurant_name, cuisine_type):
        self.restaurant_name = restaurant_name
        self.cuisine_type = cuisine_type

    # prints details
    def describe_restaurant(self):
        print(f"{self.restaurant_name} serves {self.cuisine_type} food.")

    # prints open message
    def open_restaurant(self):
        print(f"{self.restaurant_name} is now open!")


# make an object
restaurant = Restaurant("Jollibee", "Fast Food")

print(restaurant.restaurant_name)
print(restaurant.cuisine_type)

restaurant.describe_restaurant()
restaurant.open_restaurant()


