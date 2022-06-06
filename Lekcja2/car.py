class Car:

    def __init__(self, fuel, maxspeed):
        self.fuel = fuel
        self.maxspeed = maxspeed

    def refuel(self, amount):
        self.fuel += amount

    def drive(self):
        if self.fuel > 0:
            print("Driving")
            self.fuel -= 1
        else:
            print("No fuel")


polo = Car(20, 185)
mini = Car(10, 170)
beetle = Car(0, 150)

print("Polo has " + str(polo.fuel) + " of fuel")
polo.drive()
print("Polo has " + str(polo.fuel) + " of fuel")

print("---")
print("Beetle has " + str(beetle.fuel) + " of fuel")
beetle.drive()

print("---")
print("Mini has " + str(mini.fuel) + " of fuel")
