import pandas as pd
from sqlalchemy import create_engine

# 1. Build the connection bridge to your MySQL database
# Format: mysql+mysqlconnector://user:password@host/database
# Change 'YOUR_ROOT_PASSWORD' to your actual MySQL password!
from sqlalchemy import create_engine

# Using a URL object completely prevents the double-@ sign confusion!
from sqlalchemy.engine import URL

connection_url = URL.create(
    drivername="mysql+mysqlconnector",
    username="root",
    password="YOUR_ROOT_PASSWORD",  # Your password fits perfectly here now
    host="localhost",
    database="apex_fitness"
)

engine = create_engine(connection_url)

# 2. Write the SQL Query to pull class booking statistics
query = """
SELECT 
    c.class_name,
    c.capacity,
    COUNT(b.booking_id) AS current_bookings
FROM Classes c
LEFT JOIN Bookings b ON c.class_id = b.class_id
GROUP BY c.class_id, c.class_name, c.capacity;
"""

# 3. Pull the data out of MySQL and automatically load it into a Pandas DataFrame
df = pd.read_sql(query, con=engine)

# 4. Display the raw DataFrame in the console
print("\n--- 📊 RAW DATAFRAME FROM MYSQL ---")
print(df)

# 5. Use Pandas to calculate a new column: Occupancy Rate percentage
df['occupancy_rate'] = (df['current_bookings'] / df['capacity']) * 100

print("\n--- 📈 PANDAS PROCESSED DATA (Occupancy Rate Included) ---")
print(df)

import matplotlib.pyplot as plt

# Tell Pandas to plot a bar chart using our data
df.plot(x='class_name', y='occupancy_rate', kind='bar', color='skyblue', legend=False)
plt.title('Apex Fitness Class Occupancy Rates')
plt.ylabel('Occupancy Rate (%)')
plt.xlabel('Class Name')
plt.xticks(rotation=45)
plt.tight_layout()

# Make the window pop up!
plt.show()
