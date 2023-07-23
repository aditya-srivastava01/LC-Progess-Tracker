import mysql.connector
import matplotlib.pyplot as plt
import numpy as np

# Assuming 'data' is a list of dictionaries containing user data
# Each dictionary should have keys: 'user_id', 'score',"Q1->'$.finish_time'", "Q2->'$.finish_time'", "Q3->'$.finish_time'", "Q4->'$.finish_time'"

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
query = "SELECT rnk,user_id, finish_time->'$.finish_time',Q1->'$.finish_time',Q2->'$.finish_time',Q3->'$.finish_time',Q4->'$.finish_time' FROM weekly351;"
cursor.execute(query)

# Fetch the data
data = cursor.fetchall()

# Filter data for user_id='Aditya001'
user_data = [entry for entry in data if entry['user_id'] == 'Aditya001']

# Convert finish times to minutes
def convert_to_minutes(time_str):
    try:
        return int(time_str) // 60
    except ValueError:
        return 0

q1_finish_time_user = convert_to_minutes(user_data[0]["Q1->'$.finish_time'"])
q2_finish_time_user = convert_to_minutes(user_data[0]["Q2->'$.finish_time'"])
q3_finish_time_user = convert_to_minutes(user_data[0]["Q3->'$.finish_time'"])
q4_finish_time_user = convert_to_minutes(user_data[0]["Q4->'$.finish_time'"])

# Filter data for other users (excluding 'Aditya001')
other_users_data = [entry for entry in data if entry['user_id'] != 'Aditya001']

# Calculate the average finish times for other users for Q1, Q2, Q3, and Q4, excluding 0 values
q1_finish_times_others = [convert_to_minutes(entry["Q1->'$.finish_time'"]) for entry in other_users_data if entry["Q1->'$.finish_time'"] != '0']
q2_finish_times_others = [convert_to_minutes(entry["Q2->'$.finish_time'"]) for entry in other_users_data if entry["Q2->'$.finish_time'"] != '0']
q3_finish_times_others = [convert_to_minutes(entry["Q3->'$.finish_time'"]) for entry in other_users_data if entry["Q3->'$.finish_time'"] != '0']
q4_finish_times_others = [convert_to_minutes(entry["Q4->'$.finish_time'"]) for entry in other_users_data if entry["Q4->'$.finish_time'"] != '0']

# Calculate the mean for each problem for other users
avg_q1_finish_time_others = np.mean(q1_finish_times_others)
avg_q2_finish_time_others = np.mean(q2_finish_times_others)
avg_q3_finish_time_others = np.mean(q3_finish_times_others)
avg_q4_finish_time_others = np.mean(q4_finish_times_others)

# Create x-coordinates for the vertical lines
x_user = []
x_others = []

# Create y-coordinates for the vertical lines
y_user = []
y_others = []

# Add points for 'Aditya001' only if finish time is not 0
if q1_finish_time_user != 0:
    x_user.append(1)
    y_user.append(q1_finish_time_user)
else:
    plt.plot(1, 0, marker='o', markersize=8, label='Not Solved', color='red')

if q2_finish_time_user != 0:
    x_user.append(2)
    y_user.append(q2_finish_time_user)
else:
    plt.plot(2, 0, marker='o', markersize=8, label='Not Solved', color='red')

if q3_finish_time_user != 0:
    x_user.append(3)
    y_user.append(q3_finish_time_user)
else:
    plt.plot(3, 0, marker='o', markersize=8, label='Not Solved', color='red')

if q4_finish_time_user != 0:
    x_user.append(4)
    y_user.append(q4_finish_time_user)
else:
    plt.plot(4, 0, marker='o', markersize=8, label='Not Solved', color='red')

# Add points for average finish times of other users only if they are not 0
if avg_q1_finish_time_others != 0:
    x_others.append(1)
    y_others.append(avg_q1_finish_time_others)

if avg_q2_finish_time_others != 0:
    x_others.append(2)
    y_others.append(avg_q2_finish_time_others)

if avg_q3_finish_time_others != 0:
    x_others.append(3)
    y_others.append(avg_q3_finish_time_others)

if avg_q4_finish_time_others != 0:
    x_others.append(4)
    y_others.append(avg_q4_finish_time_others)

# Set the y-axis limits from 0 to a minimum of 90 minutes and maximum value from the data
plt.ylim(0, max(90, max(y_user)))

# Plot the finish times of 'Aditya001' and average finish times of other users as vertical lines for all four problems
plt.plot(x_user, y_user, marker='o', linestyle='-', color='b', label='Aditya001')
plt.plot(x_others, y_others, marker='o', linestyle='-', color='g', label='Average for Other Users')
plt.xticks([1, 2, 3, 4], ['Q1', 'Q2', 'Q3', 'Q4'])
plt.xlabel('Problems')
plt.ylabel('Finish Time (Minutes)')
plt.title('Finish Times of Aditya001 vs. Average Finish Times for Other Users')
plt.legend()
plt.grid(True)
plt.show()
