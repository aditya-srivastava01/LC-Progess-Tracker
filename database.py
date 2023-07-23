import mysql.connector

# MySQL connection details
config = {
    'user': 'root',
    'password': '0000',
    'host': 'localhost',
    'database': 'leetcode'
}

# Connect to MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Execute SQL commands

for i in range(1, 1001):
    query = f"CREATE TABLE weekly{i}(rnk INT PRIMARY KEY, user_id VARCHAR(120), score INT, finish_time JSON, Q1 JSON, Q2 JSON, Q3 JSON, Q4 JSON);"
    cursor.execute(query)
    print(f"Successfully created: weekly_{i}")

# Commit and close the connection
conn.commit()
cursor.close()
conn.close()
