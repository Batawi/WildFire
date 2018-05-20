from random import *
import random
import copy
import sys
from tkinter import *


window_width = 800 #in pixels
window_height = 600 #in pixels
map_width = 50 #number of cells
map_height = 50 #number of cells
scale = 10
time_stamp = 1000 #time_stamp[ms] = 1[min] of simulation


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
        self.grid = [[0 for x in range(width+2)] for y in range(height+2)]
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

        self.canvas.after(time_stamp, self._updateTexts)

    def generateRandomMap(self, materials):
        for i in range(1, map_height+1):
            for j in range(1, map_width+1):
                self.grid[i][j] = Cell(copy.copy(random.choice(materials)), randint(0, 10), randint(5, 35), 0, randint(0, 100))

    def randomCosmicGenerator(self, materials):
        # water border
        for i in range(0, map_height+2):
            self.grid[i][0] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
            self.grid[i][map_width+1] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
        for i in range(0, map_width+2):
            self.grid[0][i] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
            self.grid[map_height+1][i] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)

        # Grass/Bushes/logs
        for i in range(1,map_height+1):
            for j in range(1,map_width+1):
                if randint(0, 8) == 3: # Log -> 12,5%
                    self.grid[i][j] = Cell(copy.copy(materials[2]), 3, 22, 0, 17)
                elif randint(0, 2) == 1: # Bush -> 17,5%
                    self.grid[i][j] = Cell(copy.copy(materials[3]), 3, 22, 0, 17)
                else: # Grass -> rest
                    self.grid[i][j] = Cell(copy.copy(materials[1]), 3, 22, 0, 17)

        #Trees  # Trees overwrite
                # current cell with 25%
        for i in range(2, map_height):
            for j in range(2, map_width):
                if randint(0, 3) == 1:
                    self.grid[i][j] = Cell(copy.copy(materials[4]), 3, 22, 0, 17)

        #Water  # Can occur 1 to 4 times,
                # it will spread untill
                # reach end of the map
        quantity = randint(1, 4)
        for o in range(0, quantity):

            # random starting point
            i = randint(5, map_height - 1)
            j = randint(5, map_width - 1)
            self.grid[i][j] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)

            # GOD MACHINE FOR MAKING WATER
            while 1:
                if i+1 >= map_height or j+1 >= map_width or j <= 0: break
                else:
                    self.grid[i + 1][j + 1] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
                    self.grid[i + 1][j - 1] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
                    self.grid[i + 1][j] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
                    self.grid[i][j + 1] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)

                if i-1 <= 0 or j-1 <= 0 or j >= map_width: break
                else:
                    self.grid[i - 1][j + 1] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
                    self.grid[i - 1][j - 1] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
                    self.grid[i - 1][j] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)
                    self.grid[i][j - 1] = Cell(copy.copy(materials[0]), 10, 12, 0, 12)

                #  direction of spread
                test = randint(0, 10)
                if test < 4:
                    j += 1
                if test > 6:
                    j -= 1
                if test % 3 == 0:
                    i += 1
                if test == 5:
                    test = test
                if test % 3 == 1:
                    i -= 1

    def drawMap(self):
        x_off = window_width/2 - map_width*scale/2
        y_off = window_height/2 - map_height*scale/2
        for i in range(0, map_height+2):
            for j in range(0, map_width+2):
                #col = "#%03x"%randint(0, 0xFFF)
                col = self.grid[i][j].material.color
                self.canvas.create_rectangle(j*scale+x_off, i*scale+y_off, (j+1)*scale+x_off, (i+1)*scale+y_off, fill=col)

        self.canvas.pack()
        self.canvas.after(time_stamp, self.drawMap)

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

        self.canvas.after(time_stamp, self.setWind)

    def ignition(self):
        found = 0
        while found == 0:
            x = randint(1, map_width)
            y = randint(1, map_height)
            if(self.grid[y][x].material.state == 1):
                found = 1
                self.grid[y][x].material.state = 2
                self.grid[y][x].material.color = "#ff0000"
                print("ogien x: ", x, " y: ", y)
                break

    def simulation(self):
        print("symulacja")
        update_array = [[0 for x in range(map_width+2)] for y in range(map_height+2)]

        for i in range(1, map_height+1):
            for j in range(1, map_width+1):
                if(self.grid[i][j].material.state == 2): #burning
                    # --- FLASH POINT IGNITION ---
                    temp = self.grid[i][j].material.burning_temp #temp of current cell

                    if(self.grid[i-1][j-1].material.state == 1 and
                    self.grid[i-1][j-1].material.flash_point_temp <= temp):
                        update_array[i-1][i-1] = 1

                    if(self.grid[i-1][j].material.state == 1 and
                    self.grid[i-1][j].material.flash_point_temp <= temp):
                        update_array[i-1][j] = 1

                    if(self.grid[i-1][j+1].material.state == 1 and
                    self.grid[i-1][j+1].material.flash_point_temp <= temp):
                        update_array[i-1][j+1] = 1

                    if(self.grid[i][j-1].material.state == 1 and
                    self.grid[i][j-1].material.flash_point_temp <= temp):
                        update_array[i][j-1] = 1

                    if(self.grid[i][j+1].material.state == 1 and
                    self.grid[i][j+1].material.flash_point_temp <= temp):
                        update_array[i][j+1] = 1

                    if(self.grid[i+1][j-1].material.state == 1 and
                    self.grid[i+1][j-1].material.flash_point_temp <= temp):
                        update_array[i+1][j-1] = 1

                    if(self.grid[i+1][j].material.state == 1 and
                    self.grid[i+1][j].material.flash_point_temp <= temp):
                        update_array[i+1][j] = 1

                    if(self.grid[i+1][j+1].material.state == 1 and
                    self.grid[i+1][j+1].material.flash_point_temp <= temp):
                        update_array[i+1][j+1] = 1


        for i in range(1, map_height+1):
            for j in range(1, map_width+1):
                if(update_array[i][j] == 1):
                    self.grid[i][j].material.state = 2
                    self.grid[i][j].material.color = "#ff0000"

        self.canvas.after(time_stamp, self.simulation)



# ---- FUNCTIONS ----

# ---- MATERIALS ----
#fuel[min], auto ign[temp], flash point[temp], state, burning_temp[temp], color
materials = [] #new materials can be add freerly
materials.append(Material("Water", 0, 0, 0, 0, 0, "#0099ff"))
materials.append(Material("DryGrass", 5, 300, 500, 1, 400, "#ffcc66"))
materials.append(Material("Log", 15, 500, 700, 1, 500, "#666633"))
materials.append(Material("Bush", 15, 500, 300, 1, 600, "#99cc00"))
materials.append(Material("Tree", 1000, 750, 30, 1, 1100, "#009933"))

# ---- MAIN ----

#window init
root = Tk()
root.title = "WildFire Simulator"
canvas = Canvas(root, width = window_width, height = window_height)
canvas.pack()

#map class object init
area = Map(map_width, map_height, canvas)

#start simulation

#area.generateRandomMap(materials)
area.randomCosmicGenerator(materials)
area.ignition()

area.simulation()

area.drawMap()
area.setWind()
area.showClassVariables()

#loop start
root.mainloop()
