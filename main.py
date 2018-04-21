from random import *
import random
import copy
import sys
from Tkinter import *


window_width = 800 #in pixels
window_height = 600 #in pixels
map_width = 20 #number of cells
map_height = 10 #number of cells
scale = 25

# ---- CLASSES ----

class Material:
    index = 0 #number of created materials

    def __init__(self, name, fuel, auto_ignition_temp, flash_point_temp, state, burning_temp, color):
        Material.index = Material.index + 1
        self.name = name
        self.fuel = fuel #hit points, minutes of burning
        self.auto_ignition_temp = auto_ignition_temp #in Celsius
        self.flash_point_temp = flash_point_temp
        self.state = state
        self.id = Material.index
        self.color = color
        self.burning_temp = burning_temp

        #state:
        #0 cannot burn
        #1 can burn
        #2 burning
        #3 burned

class Cell:

    def __init__(self, material, humidity, temp, downfall, height):
        self.material = material
        self.humidity = humidity #from 0 to 10
        self.temp = temp
        self.downfall = downfall
        self.height = height

        #downfall
        # <-10, -1> snow
        # 0 nothing
        # <1, 10> rain

class Map:

    def __init__(self, width, height, canvas):
        self.canvas = canvas
        self.grid = [[0 for x in range(width)] for y in range(height)]
        self.wind_dir = randint(0, 359) #integer degree, cycling
        self.wind_power = randint(0 , 12) #beaufort
        self.texts_to_update = []

    # ---- METODY ----

    def showClassVariables(self): #dont use in case of static texts
        self.texts_to_update.append(self.canvas.create_text(10, 10, fill="darkblue", font="Monospace 13", text="", anchor="nw"))

        self.texts_to_update.append(self.canvas.create_text(10, 25, fill="darkblue", font="Monospace 13", text="", anchor="nw"))

        self._updateTexts()

    def _updateTexts(self): #private method, dont use outside
        self.canvas.itemconfig(self.texts_to_update[0], text="dir: "+str(self.wind_dir))
        self.canvas.itemconfig(self.texts_to_update[1], text="power: "+str(self.wind_power))

        self.canvas.after(100, self._updateTexts)

    def generateRandomMap(self, materials):
        for i in range(0, map_height):
            for j in range(0, map_width):
                self.grid[i][j] = Cell(copy.copy(random.choice(materials)), randint(0, 10), randint(5, 35), 0, randint(0, 100))

    def drawMap(self):
        x_off = window_width/2 - map_width*scale/2
        y_off = window_height/2 - map_height*scale/2
        for i in range(0, map_height):
            for j in range(0, map_width):
                col = "#%03x"%randint(0, 0xFFF)
                #col = self.grid[i][j].material.color
                self.canvas.create_rectangle(j*scale+x_off, i*scale+y_off, (j+1)*scale+x_off, (i+1)*scale+y_off, fill=col)

        #canvas.create_rectangle(300, 300, 200, 10, fill="blue", outline="blue")
        self.canvas.pack()
        self.canvas.after(500, self.drawMap)

    def setWind(self):
        w_dir = random.choice([-1, 0, 1])
        #w_pow = random.choice([-1, 0, 0, 0, 0, 0, 0, 0, 1]) #sila wiatru bedzie sie zmieniac wolniej
        w_pow = randint(-20, 20)

        if w_dir == 1 and self.wind_dir == 359:
            self.wind_dir = 0
        elif  w_dir == -1 and self.wind_dir == 0:
            self.wind_dir = 359
        else:
            self.wind_dir += w_dir

        if w_pow == 1 and self.wind_power == 12:
            self.wind_power = 12
        elif w_pow == -1 and self.wind_power == 1:
            self.wind_power = 1
        elif w_pow == 1:
            self.wind_power += 1
        elif w_pow == -1:
            self.wind_power -= 1


        self.canvas.after(100, self.setWind)

# ---- FUNCTIONS ----

# ---- MATERIALS ----

#fuel, auto ign, flash point, state, color
materials = [] #new materials can be add freerly
materials.append(Material("Water", 0, 0, 0, 0, 0, "#0099ff"))
materials.append(Material("DryGrass", 5, 300, 5, 1, 400, "#ffcc66"))
materials.append(Material("Log", 15, 500, 10, 1, 500, "#666633"))
materials.append(Material("Bush", 15, 500, 15, 1, 600, "#99cc00"))
materials.append(Material("Tree", 1000, 1000, 30, 1, 1100, "#009933"))

# ---- MAIN ----

#window init
root = Tk()
root.title = "WildFire Simulator"
canvas = Canvas(root, width = window_width, height = window_height)
canvas.pack()

#map class object init
area = Map(map_width, map_height, canvas)

#methods start
area.generateRandomMap(materials)
area.drawMap()
area.setWind()

area.showClassVariables()

#loop start
root.mainloop()
