from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pyplot as plt
import time
import numpy as np


# Model parameters
time_step = 1          # simulation time step in days
start_time = 0         # in days
end_time = 365*2         # in days
start_hM = 500         # starting number of healthy Mosquitoes 
start_iM = 10           # starting number of infected Mosquitoes 
start_hV = 4500      # starting number of healthy Villagers
start_sV = 100           # starting number of sick Villagers
start_iV = 0           # starting number of immune Villagers

# Villager rate parameters
brV = .019/365         # birth rate of Villagers
drV = .008/365         # death rate of Villagers
midrV = 0.001986       # malaria induced death rate of Villagers
rrV = 0.3              # recovery rate of Villagers
irV = 0.01             # immunity rate of Villagers

# Mosquito rate parameters
brM = 0.01             # birth rate of Mosquitoes
drM = 0.01             # death rate of Mosquitoes
brfM = 0.3             # bite rate from Mosquitoes


# Derived constants
N = int((end_time - start_time) / time_step)    # number of simulation steps

# Time-varying quantities, arrays with one value per time step
# The syntax, "[0]*(N+1)," creates a one-dimensional array of length N+1 whose values are all zero.
t = [0]*(N+1)        # time in days

V = [0]*(N+1)        # total Villagers
hV = [0]*(N+1)       # healthy Villagers
sV = [0]*(N+1)       # sick Villagers
iV = [0]*(N+1)       # immune Villagers

M = [0]*(N+1)        # total Mosquitoes 
hM = [0]*(N+1)       # healthy Mosquitoes 
iM = [0]*(N+1)       # infected Mosquitoes

# Initialize and derive variables
t[0] = start_time

hV[0] = start_hV
sV[0] = start_sV
iV[0] = start_iV
V[0] = start_hV + start_sV + start_iV       # Total villager population

hM[0] = start_hM
iM[0] = start_iM
M[0] = start_hM + start_iM      # Total mosquito population



# Define function to update the number of current healthy villagers
# Healthy Villagers = 
#     = Currently healthy Villagers 
#     + Births
#     + Recovered in this time step
#     - Deaths of currently healthy Villagers
#     - Infected in this time step
def Healthy_Villagers ( i, hV, sV, brV, drV, rrV, M, iM, brfM ) :
    hV[i+1] = hV[i] + (hV[i] * brV) + (sV[i] * rrV) - (hV[i] * drV) - (hV[i] * brfM * (iM[i] / M[i]))


# TODO: Update current sick villagers
# Sick Villagers = 
#     = Current number of sick villagers
#     + Became infected in this time step
#     - Deaths of currently sick Villagers
#     - Recovered in this time step
#     - Became immune in this time step
def Sick_Villagers ( i, hV, sV, rrV, irV, drV, M, iM, brfM ) :
    sV[i+1] = sV[i] - sV[i]*(rrV+irV+drV+midrV) + (hV[i] * brfM * (iM[i] / M[i]))
    

# TODO: Update current immune villagers
# Immune Villagers = 
#     = Current number of immune Villagers
#     + Became immune in this time step
#     - Deaths of currently immune Villagers
def Immune_Villagers ( i, iV, sV, irV, drV ) :
    iV[i+1] = iV[i] - iV[i] * drV + sV[i]*irV

# TODO: Update current healthy mosquitoes
# Healthy Mosquitoes =
#     = Current number of healthy Mosquitoes
#     + Mosquito Births
#     - Deaths of currently healthy Mosquitoes
#     - Infected in this time step
def Healthy_Mosquitoes ( i, V, sV, M, hM, brM, drM, brfM ) :
    hM[i+1] = (1 + brM - drM -brfM*(sV[i]/V[i]))*hM[i]
    

# TODO: Update current infected Mosquitoes
# Infected Mosquitoes = 
#     = Current number of infected Mosquitoes
#     + Infected in this time step
#     - Deaths of currently infected Mosquitoes
def Infected_Mosquitoes ( i, V, sV, hM, iM, drM, brfM ) :
  iM[i+1] = (1 + brfM*(sV[i]/V[i]) - drM)*iM[i]

# A for loop that updates human and mosquito populations for a given
# simulation step
for i in range(N):
    t[i+1] = t[i] + time_step
    
    Healthy_Villagers ( i, hV, sV, brV, drV, rrV, M, iM, brfM )
    
    Sick_Villagers ( i, hV, sV, rrV, irV, drV, M, iM, brfM )
    
    Immune_Villagers ( i, iV, sV, irV, drV )
    
    Healthy_Mosquitoes ( i, V, sV, M, hM, brM, drM, brfM )
    
    Infected_Mosquitoes ( i, V, sV, hM, iM, drM, brfM )
    
    # Update current total humans
    V[i+1] = hV[i]+ sV[i] + iV[i]    
    
    # Update current total mosquitoes    
    M[i+1] = hM[i] + iM[i]
    
# Now plot the results on two separate graphs
plt.figure()
plt.title('Healthy/Sick/Immune Villagers vs Time')
plt.ylabel('Population')
plt.xlabel('Time (Days)')

plt.plot(t,hV, color = "blue", label = "Healthy Villagers" )
plt.plot(t,sV, color="red", label = "Sick Villagers")
plt.plot(t,iV, color="green", label = "Immune Villagers")

plt.legend(loc='upper right')

plt.minorticks_on()

plt.show()



#plot 2
plt.figure()
plt.title('Healthy/Infected Mosquitoes vs Time')
plt.ylabel('Mosquitoes')
plt.xlabel('Time (Days)')

plt.plot(t, hM, label = "Healthy Mosquitoes" )
plt.plot(t, iM, color="red", label = "Infected Mosquitoes ")

plt.legend(loc='center right')

plt.minorticks_on()

plt.show()