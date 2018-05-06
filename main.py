from random import randint
import copy
import sys
from tkinter import *


window_width = 1200 #in pixels
window_height = 1200 #in pixels
map_width = 200 #number of cells
map_height = 200 #number of cells
scale = 5

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

    # ---- METODY ----

    def generateRandomMap(self, materials):
        for i in range(0, map_height):
            for j in range(0, map_width):
                self.grid[i][j] = Cell(copy.copy(materials[randint(0, len(materials)-1)]), randint(0, 10), randint(5, 35), 0, randint(0, 100))

    def randomCosmicGenerator(self, materials):

        # Grass/Bushes/logs
        for i in range(0,map_height):
            for j in range(0,map_width):
                if randint(0, 8) == 3:                                                  # Log -> 12,5%
                    self.grid[i][j] = Cell(copy.copy(materials[2]), 3, 22, 0, 17)
                elif randint(0, 2) == 1:                                                # Bush -> 17,5%
                    self.grid[i][j] = Cell(copy.copy(materials[3]), 3, 22, 0, 17)
                else:                                                                   # Grass -> rest
                    self.grid[i][j] = Cell(copy.copy(materials[1]), 3, 22, 0, 17)

        #Trees                                                                          # Trees overwrite
                                                                                        # current cell with 25%
        for i in range(1, map_height - 1):
            for j in range(1, map_width - 1):
                if randint(0, 3) == 1:
                    self.grid[i][j] = Cell(copy.copy(materials[4]), 3, 22, 0, 17)

        #Water                                                                          # Can occur 1 to 4 times,
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
        for i in range(0, map_height):
            for j in range(0, map_width):
                #col = "#%03x"%randint(0, 0xFFF)
                col = self.grid[i][j].material.color
                self.canvas.create_rectangle(j*scale+x_off, i*scale+y_off, (j+1)*scale+x_off, (i+1)*scale+y_off, fill=col)

        #canvas.create_rectangle(300, 300, 200, 10, fill="blue", outline="blue")
        self.canvas.pack()
        self.canvas.after(500, self.drawMap)

    def setWind(self):
        w_dir = randint(-1, 1)
        w_pow = randint(1, 12)

        #if w_dir == 1 AND self.wind_dir == 359
            #self.wind_dir


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

#window initburning_temp
root = Tk()
root.title = "WildFire Simulator"
canvas = Canvas(root, width = window_width, height = window_height)
canvas.pack()

area = Map(map_width, map_height, canvas)
# area.generateRandomMap(materials)
area.randomCosmicGenerator(materials)
area.drawMap()
root.mainloop()



#print("--- jestesmy tutaj ---")





'''

for i in range(0, map_height):
    for j in range(0, map_width):
        sys.stdout.write(str(area.grid[i][j].material.fuel))
        sys.stdout.write("   ")
    print("")


TODO:

CUDA
1. Stworzyc 5 materialow
2. Stworzyc mape, na poczatek moze to byc totalny random
3. Zrobic metody, glownie w klasie Map poniewaz bedziemy operowac na Cella'ach
4. Zrobic jakies wyswietlanie
5. losowanie sily wiatru nie powinno byc rowno prawdopodobne dla wszystkich wartosci

Notes:
1. Docelowo wielkosc mapy ma byc okolo full HD (1920/1080)
2. Wiatr ma byc staly, jednolity na cala mape
3. Ogien na danej kratce przestaje sie palic tylko w dwoch wypadkach:
- wypali sie paliwo
- opad atmosferyczny zgasi ogien, jesli tak to ilosc paliwa pozostaje taka jak w ostatnim
momencie palenia i zwieksza sie bardzo wilgotnosc
4. Im wyzsza temperatura ognia tym szybciej wypala on paliwo
5. Ogien rozprzestrzenia sie szybciej w kierunu wyzszych terenow oraz w kierunku wiania wiatru
6. Auto ignition jest to temperatura w ktorej nastepuje samozaplon
7. Flash point jest to temperatura w ktorej material podpala sie od otwartego ognia
8. Jeden cykl odpowiada jednej minucie
9. Kiedy kratka bedzie sie palic bedzie to sygnalizowane migajacym kolorem, im wolniej
    miga tym mniej jest paliwa na danej kratce a kolor materialu dazy do czarnego


oddawanie do max 21.05
git
'''
