import pandas as pd
import sqlite3

df = pd.read_csv("drinks.csv")
print(df)

conn = sqlite3.connect("drinks.db")


# Save CSV data to SQLite
df.to_sql("drinks", conn, if_exists="replace", index=False) #переносить дані з pandas DataFrame у таблицю SQLite.

print("Data saved successfully!")

# Close database connection
conn.close()
