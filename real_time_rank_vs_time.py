import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


# Assuming 'data' is a list of dictionaries containing user data
# Each dictionary should have keys: 'user_id', 'score',"Q1->'$.finish_time'", "Q2->'$.finish_time'", "Q3->'$.finish_time'", "Q4->'$.finish_time'"
def custom_sort(item):
    return (-item[0], item[1],item[2])

# Database connection parameters
config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': 'leetcode'
}

# Connect to the database
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)

# Query to fetch the data
query = "SELECT rnk,user_id,score, finish_time->'$.finish_time',Q1->'$.finish_time',Q2->'$.finish_time',Q3->'$.finish_time',Q4->'$.finish_time',Q1->'$.wa',Q2->'$.wa',Q3->'$.wa',Q4->'$.wa' FROM weekly354;"
cursor.execute(query)

# Fetch the data
data = cursor.fetchall()
print(len(data))
# Filter data for user_id='Aditya001'
user_data = [entry for entry in data if entry['user_id'] == 'Aditya001']

# Convert finish times to minutes
def convert_to_minutes(time_str):
    try:
        return int(time_str) // 60
    except ValueError:
        return 0

# Create the time intervals at 5-minute intervals from 1 to 91
time_intervals = list(range(1, 150,5))

# Calculate the rank at each time interval of 5 minutes
ranks = []
rank_user = []
for time_interval in time_intervals:
    rank = []
    user_id = ""
    for entry in data:
        points = 0
        total_time = 0
        user_id = entry["user_id"]
        if int(entry["Q1->'$.finish_time'"])!=0 and int(entry[f"Q{1}->'$.finish_time'"])<=time_interval*60:
            points += 3
            total_time = max(total_time,int(entry["Q1->'$.finish_time'"])) + int(entry["Q1->'$.wa'"])*5*60
        if int(entry["Q2->'$.finish_time'"])!=0 and int(entry[f"Q{2}->'$.finish_time'"])<=time_interval*60:
            points += 4
            total_time = max(total_time,int(entry["Q2->'$.finish_time'"])) + int(entry["Q2->'$.wa'"])*5*60
        if int(entry["Q3->'$.finish_time'"])!=0 and int(entry[f"Q{3}->'$.finish_time'"])<=time_interval*60:
            points += 4
            total_time = max(total_time,int(entry["Q3->'$.finish_time'"])) + int(entry["Q3->'$.wa'"])*5*60
        if int(entry["Q4->'$.finish_time'"])!=0 and int(entry[f"Q{4}->'$.finish_time'"])<=time_interval*60:
            points += 6
            total_time = max(total_time,int(entry["Q4->'$.finish_time'"])) + int(entry["Q4->'$.wa'"])*5*60
        rank.append([points,total_time,entry['user_id']])
    rank.sort(key=custom_sort)
    # print(len(rank))
    for i in range(0,len(rank)):
        if(rank[i][2]=="Aditya001"):
            # print(rank[i],f"at time interval : {time_interval} rank : {i+1}")
            rank_user.append([rank[i][0],rank[i][1],i+1])
            break
    ranks.append(rank)



# Plot the real-time graph of rank vs time for 'Aditya001'
sorted_times = [0]+time_intervals
sorted_ranks = [0]+[rank_of_user[2] for rank_of_user in rank_user]
print(sorted_times)
print(sorted_ranks)

# Create the figure and axis objects
fig, ax = plt.subplots()

# Define the line plot
line, = ax.plot([], [], marker='o')

# Set axis limits and labels
ax.set_xlim(0, max(time_intervals)+10)
ax.set_ylim(0, 10000)  # Adjust the y-axis limit to accommodate all possible ranks
ax.set_xlabel('Total Time')
ax.set_ylabel('Rank')
ax.set_title('Rank vs Time for User Aditya001')
ax.grid(True)

# Define the initialization function for the animation
def init():
    line.set_data([], [])
    return line,

# Define the update function for the animation
def update(frame):
    x_data = sorted_times[:frame+1]
    y_data = sorted_ranks[:frame+1]
    line.set_data(x_data, y_data)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(sorted_times), init_func=init, blit=True, repeat=False)

# Show the plot and the animation
plt.show()