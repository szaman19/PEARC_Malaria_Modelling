from __future__ import absolute_import, division, print_function, unicode_literals
import matplotlib.pyplot as plt
import time
import numpy as np

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
def Sick_Villagers ( i, hV, sV, rrV, irV, drV, midrV, M, iM, brfM) :
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
    hM[i+1] = (1 - drM-brfM*(sV[i]/V[i]))*hM[i] + ( brM  ) * M[i]
    

# TODO: Update current infected Mosquitoes
# Infected Mosquitoes = 
#     = Current number of infected Mosquitoes
#     + Infected in this time step
#     - Deaths of currently infected Mosquitoes
def Infected_Mosquitoes ( i, V, sV, hM, iM, drM, brfM ) :
  iM[i+1] = (1 + brfM*(sV[i]/V[i]) - drM)*iM[i]

def sim(params):
	# Model parameters
	time_step = 1          # simulation time step in days
	start_time = params['start_time']        # in days
	end_time = params['end_time']        # in days
	start_hM = params['hM']         # starting number of healthy Mosquitoes 
	start_iM = params['iM']          # starting number of infected Mosquitoes 
	start_hV = params['hV']      # starting number of healthy Villagers
	start_sV = params['sV']           # starting number of sick Villagers
	start_iV = params['iV']          # starting number of immune Villagers

	# Villager rate parameters
	brV = params['brV']/365         # birth rate of Villagers
	drV = params['drV']/365         # death rate of Villagers
	midrV = params['midrV']       # malaria induced death rate of Villagers
	rrV = params['rrV']           # recovery rate of Villagers
	irV = params['irV']            # immunity rate of Villagers

	# Mosquito rate parameters
	brM = params['brM']            # birth rate of Mosquitoes
	drM = params['drM']             # death rate of Mosquitoes
	brfM = params['brfM']             # bite rate from Mosquitoes


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

	death_count = [0]*(N+1)
	for i in range(N):
	    if(i < 80 or i > 200):
	    	brM = params['brM'] * 4
	    t[i+1] = t[i] + time_step
	    
	    Healthy_Villagers ( i, hV, sV, brV, drV, rrV, M, iM, brfM )
	    
	    Sick_Villagers ( i, hV, sV, rrV, irV, drV, midrV, M, iM, brfM )
	    
	    Immune_Villagers ( i, iV, sV, irV, drV )
	    
	    Healthy_Mosquitoes ( i, V, sV, M, hM, brM, drM, brfM )
	    
	    Infected_Mosquitoes ( i, V, sV, hM, iM, drM, brfM )


	    
	    # Update current total humans
	    V[i+1] = hV[i]+ sV[i] + iV[i]
	    death_count[i+1] = drV*(sV[i]+hV[i]+iV[i]) + sV[i]*midrV + death_count[i]
	    
	    # Update current total mosquitoes    
	    M[i+1] = hM[i] + iM[i]


	return t, hV, sV, iV, hM, iM, death_count

def main():
	colors= ['r','b','g', 'm']
	plt.figure()
	for i in range(1):
		params = {}
		params['start_time'] = 1      # in days
		params['end_time'] =730        # in days
		params['hM'] = 5000   # starting number of healthy Mosquitoes 
		params['iM'] = 1000     # starting number of infected Mosquitoes 
		params['hV'] = 1000   # starting number of healthy Villagers
		params['sV'] = 100       # starting number of sick Villagers
		params['iV'] = 0    # starting number of immune Villagers
	
			# Villager rate parameters
		params['brV'] =  0.019       # birth rate of Villagers
		params['drV'] =  0.008      # death rate of Villagers
		params['midrV'] = 0.0019986      # malaria induced death rate of Villagers
		params['rrV']  = 0.3        # recovery rate of Villagers
		params['irV']  = 0.01         # immunity rate of Villagers

	# Mosquito rate parameters
		params['brM']  =0.01         # birth rate of Mosquitoes
		params['drM']  =0.01      # death rate of Mosquitoes
		params['brfM'] =0.3       # bite rate from Mosquitoes

		t, hV, sV, iV, hM, iM, DC = sim(params)
		plt.title('Healthy / Sick/ Immune/ Dead Villagers vs Time')
		plt.ylabel('Population')
		plt.xlabel('Time (Days)')
		plt.plot(t,sV, color=colors[i],label =" Sick people" )
		plt.plot(t,hV,  color=colors[i+1],label = " Healthy People" )
		plt.plot(t,iV, color=colors[i+2],label = " Immune people" )
		plt.plot(t,DC, color='black', label=" Dead People")
		plt.legend()
		plt.show()
		# print("Death Counter: ", DC)
		plt.figure()
		plt.title('Healthy/Infected Mosquitoes vs Time')
		plt.ylabel('Mosquitoes')
		plt.xlabel('Time (Days)')

		plt.plot(t, hM, label = "Healthy Mosquitoes" )
		plt.plot(t, iM, color="red", label = "Infected Mosquitoes ")

		plt.legend(loc='center right')

		plt.minorticks_on()

		plt.show()
		
	
	# plt.show()

main()		
