
from mainWindow import MainWindow
from numpy import random

class Sensor():

    def __init__(self):
        self.map_weather = random.random_sample((int(MainWindow.sw/10), int(MainWindow.sh/10)))

s = Sensor()
print(s.map_weather)