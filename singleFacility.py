import simpy
import statistics
import numpy as np
import matplotlib.pyplot as plt

totalCosts = []
avgWaiting = []
resources = []

for i in range(10000):

        server_name = "Amazon"
        server_cap = 1 #capacity
        entity_name = "Truck"
        service_times = []
        for i in range(20):
                random_service = np.random.uniform(.5, 3)
                service_times.append(random_service)
        #End input data collection

        #initialize env for sim
        q_env = simpy.Environment()

        #resource initialize
        q_res = simpy.Resource(q_env, capacity=server_cap)

        #Storing variables of each state into arrays
        waiting_times = []
        queue_lengths = []
        start_times = []
        end_times = []

        def customer(env, name, resource, arrival_time, service_time):

                yield env.timeout(arrival_time)

                #print('{} arriving at: {}'.format(name, env.now))

                with resource.request() as request:
                        yield request
                        start_time = env.now

                        #calculate waiting time
                        waiting_time = env.now - arrival_time
                        #print('{} waiting time is: {}'.format(name, waiting_time))
                        
                        #start and end service
                        #print('{} starting service at: {}'.format(name, env.now))
                        #print('Starting Queue Length : {}'.format(len(resource.queue)))
                        start_len = len(resource.queue)

                        yield q_env.timeout(service_time)

                        end_time = env.now

                        #print('{} leaving at: {}'.format(name, env.now))
                        #print('Ending Queue Length: {}'.format(len(resource.queue)))
                        end_len = len(resource.queue)


                        #add to info to arrays
                        waiting_times.append(waiting_time)
                        queue_lengths.append(start_len)
                        queue_lengths.append(end_len)
                        end_times.append(end_time)
                        start_times.append(start_time)

        def idleTime(start_arr, end_arr):
                total_idle = 0

                for i in range(len(start_arr) - 1):
                        total_idle += (start_arr[i+1] - end_arr[i])
                        
                return total_idle

        def resourceUtil(total_idle, total_time):
                busy_time = total_time - total_idle
                ratio = busy_time/total_time
                percent = ratio * 100
                return percent

        #start at time 0
        arrival_time = 0

        #number of entities
        repairs = np.random.randint(2, size=20)

        #print("REPAIRS: {}".format(repairs))

        #start simulation (main routine)
        truck_num = 1
        for i in range(20):
                arrival_time = i
                service_time = service_times[i]
                if repairs[i] == 1:
                        q_env.process(customer(q_env, (entity_name + ' {}'.format(truck_num)), q_res, arrival_time, service_time))
                        truck_num = truck_num + 1
                else:
                        continue

        q_env.run()

        #Output works but commented out for printing times sake
        # print('Minimum Queue Length = {} {}s'.format(min(queue_lengths), entity_name))
        # print('Maximum Queue Length = {} {}s'.format(max(queue_lengths), entity_name))
        # print('Total Idle Time = {} minutes'.format(idleTime(start_times, end_times)))
        # print('Resource Utilization Percent = {} %'.format(resourceUtil(idleTime(start_times, end_times), end_times[-1])))
        # print('Total Queue Time = {} minutes'.format(sum(waiting_times)))
        # print('Mean Waiting Time = {} minutes'.format(statistics.mean(waiting_times)))
        # print('Variance of Waiting Time = {} minutes'.format(statistics.variance(waiting_times)))

        #1 Facility
        busyTime = end_times[-1] - idleTime(start_times, end_times)
        cost = busyTime*5000 + end_times[-1]*2500

        totalCosts.append(cost)
        avgWaiting.append(statistics.mean(waiting_times))
        resources.append(resourceUtil(idleTime(start_times, end_times), end_times[-1]))

        sort_c = np.sort(totalCosts)

#Output
print("Average Waiting Time for 10,000 runs: {}".format(statistics.mean(avgWaiting)))
print("Average Resource Utilization for 10,000 runs: {}".format(statistics.mean(resources)))

#GRAPHING

#Cost PDF
cost_pdf = plt.figure(1)
plt.hist(sort_c, density=True, bins=30)

plt.title("1 Facility Costs PDF")
plt.xlabel("Total Costs")
plt.ylabel("Probability")

cost_pdf.show()

input("Press Enter for Cost CDF")

#Cost CDF
cost_cdf = plt.figure(2)
plt.hist(sort_c, density=True, bins=30, cumulative=True)

plt.title("1 Facility Costs CDF")
plt.xlabel("Total Costs")
plt.ylabel("Probability")

cost_cdf.show()

input()