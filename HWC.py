import math
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as sp
import re

usercurrent = (input("What would you like the current to be, in amps? "))
userlength = (input("What would you like the length of one side of the wire to be, in meters? "))

I = int(re.sub("[^0-9]", "", usercurrent))
L = int(re.sub("[^0-9]", "", userlength))

print("You want %s amps of current and the length of one side of the square loop to be %s meters." % (I, L))
print("Great! Calculating ...")

mag = [] #list of x, z magnitudes

def biosavart(x1, z1): #mag field calculation
    l_scr = np.sqrt((L/2+x1)**2+z1**2+(L/2)**2) #script r, x<0
    l_theta1 = -L/l_scr #theta1, x<0
    l_theta2 = L/l_scr #theta2, x<0
    l_biosavart = ((mu*I)/(4*math.pi*l_scr)*(math.sin(l_theta2)-math.sin(l_theta1))) #mag field from x<0, in Tesla
    lx_biosavart = l_biosavart * (z1/l_scr) #mag field from x<0, x contribution
    lz_biosavart = l_biosavart * ((L/2+x1)/l_scr) #mag field from x<0, z contribution
    r_scr = np.sqrt((L/2-x1)**2+z1**2+(L/2)**2) #script r, x>0
    r_theta1 = -L/r_scr #theta1, x>0
    r_theta2 = L/r_scr #theta2, x>0
    r_biosavart = -((mu*I)/(4*math.pi*r_scr)*(math.sin(r_theta2)-math.sin(r_theta1))) #mag field from x>0, in Tesla
    rx_biosavart = r_biosavart * (z1/r_scr) #mag field from x>0, x contribution
    rz_biosavart = r_biosavart * ((L/2-x1)/r_scr) #mag field from x>0, z contribution
    if z1 < 0:
        lz_biosavart = -(lz_biosavart) #makes z component negative
        rz_biosavart = -(rz_biosavart) #makes z component negative
    if x1 < 0:
        lx_biosavart = -(lx_biosavart) #makes x component negative
        rx_biosavart = -(rx_biosavart) #makes x component negative
        lz_biosavart = -(lz_biosavart) #makes z component negative
        rz_biosavart = -(rz_biosavart) #makes z component negative
    if x1 == 0: #filtering out solely (0, z) magnetic fields, simpler
        mag.append((0, lz_biosavart)) #B_z = one side's z contribution
        return
    elif z1 == 0: #filtering out solely (x, 0) magnetic fields, simpler
        mag.append((l_biosavart+r_biosavart, 0)) #B_x = sum of x components from both directions
        return
    elif x1 < 0: #-x calculations
        mag.append((abs(lx_biosavart+rx_biosavart), (lz_biosavart+rz_biosavart)))
        return
    elif x1 > 0: #x calculations
        mag.append(((-abs(lx_biosavart+rx_biosavart)), lz_biosavart+rz_biosavart))
        return

#generates x pairs of random integer coordinates from x to x
coords = [(x,y) for x in range(-L, L+1) for y in range(-10, 11)]
mu = sp.mu_0

x1points = [] #solely generated x coordinates
z1points = [] #solely generated z coordinates

for idx, pair in enumerate(coords):
    x1, z1 = pair
    x1points.append(x1)
    z1points.append(z1)
    biosavart(x1, z1) #run the function

plotx = [] #total x magnitude of field
plotz = [] #total z magnitude of field

for idx, points in enumerate(mag): #tuple isolation by (x, z)
    magx, magz = points
    plotx.append(magx)
    plotz.append(magz)

#plots x, z generated coordinates with x and z magnitudes
plt.quiver(x1points, z1points, plotx, plotz, width = 0.004, headwidth = 2, headlength = 4)
plt.xlim(-L, L)
plt.title('Magnetic Field for Square Loop of Current (y = 0)')
plt.xlabel('X [meters]')
plt.ylabel('Z [meters]')
plt.show()
