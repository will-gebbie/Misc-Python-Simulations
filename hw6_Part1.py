import matplotlib.pyplot as plt
import numpy as np

#Store data to push into PDF and CDF graphs
leftover_xtroops = []
leftover_ytroops = []
ending_times = []

for i in range(1000):
    alpha = np.random.uniform(0.75, 0.85)
    beta = np.random.uniform(0.85, 0.95)
    time = 0
    dt = .15 #timestep in mins

    #Total amount of soldiers in each army
    x_size = 1000
    y_size = 800

    #Initialization for Reinforcements
    rx_events = 2
    rx_occur = 0.5
    rx_size = 0.4

    ry_events = 2
    ry_occur = 0.5
    ry_size = 0.4

    #size of army when reinforcements come
    xr_occur = float(x_size * rx_occur)
    yr_occur = float(y_size * ry_occur)

    #reinforcement army sizes 
    xr_size = float(x_size * rx_size)
    yr_size = float(y_size * ry_size)

    #each side gets same amount of events
    r_events_x = int(rx_events)
    r_events_y = int(ry_events)

    #store data into lists for graphing
    x_survivors = [x_size]
    y_survivors = [y_size]
    times = [time]

    #Singular Run
    while time < 10:
        time = time + dt
        
        #Lanchester's Square Law (Aimed Fire)
        x_size = x_size - (beta * y_size)*dt 
        y_size = y_size - (alpha * x_size)*dt
        
        #trigger reinforcement for x
        if x_size <= xr_occur and r_events_x > 0:
            r_events_x = r_events_x - 1
            x_size = x_size + xr_size
            alpha = np.random.uniform(0.75, 0.85)
            
        #trigger reinforcement for y
        if y_size <= yr_occur and r_events_y > 0:
            r_events_y = r_events_y - 1
            y_size = y_size + yr_size
            beta = np.random.uniform(0.85, 0.95)
        
        #End simulation when one army hits 0
        if x_size <= 0 or y_size <=0:
            break
        
        #add tuples to array
        x_survivors.append(x_size)
        y_survivors.append(y_size)
        times.append(time)
        #end while loop
    end_xsize = x_size
    end_ysize = y_size
    end_time = time

    leftover_xtroops.append(end_xsize)
    leftover_ytroops.append(end_ysize)
    ending_times.append(end_time)

    #end for loop
    
#Sort the data
sort_x = np.sort(leftover_xtroops)
sort_y = np.sort(leftover_ytroops)
sort_t = np.sort(ending_times)

#GRAPHING SECTION

#X PDF
x_pdf = plt.figure(1)
plt.hist(sort_x, density=True, bins=30)

plt.title("X Troops PDF")
plt.xlabel("Ending X Troops")
plt.ylabel("Probability")

x_pdf.show()

input("Press Enter for next graph")

#X CDF
x_cdf = plt.figure(2)
plt.hist(sort_x, density=True, bins=30, cumulative=True)

plt.title("X Troops CDF")
plt.xlabel("Ending X Troops")
plt.ylabel("Probability")

x_cdf.show()

input("Press Enter for next graph")

#Y PDF
y_pdf = plt.figure(3)
plt.hist(sort_y, density=True, bins=30)

plt.title("Y Troops PDF")
plt.xlabel("Ending Y Troops")
plt.ylabel("Probability")

y_pdf.show()

input("Press Enter for next graph")

#Y CDF
y_cdf = plt.figure(4)
plt.hist(sort_y, density=True, bins=30, cumulative=True)

plt.title("Y Troops CDF")
plt.xlabel("Ending Y Troops")
plt.ylabel("Probability")

y_cdf.show()

input("Press Enter for next graph")

#Time PDF
t_pdf = plt.figure(5)
plt.hist(sort_t, density=True, bins=30)

plt.title("Simulation Duration")
plt.xlabel("Duration")
plt.ylabel("Probability")

t_pdf.show()

input("Press Enter for next graph")

#Time CDF
t_cdf = plt.figure(6)
plt.hist(sort_t, density=True, bins=30, cumulative=True)

plt.title("Simulation Duration")
plt.xlabel("Duration")
plt.ylabel("Probability")

t_cdf.show()

input()

