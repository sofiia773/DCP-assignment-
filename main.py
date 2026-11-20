import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

df = pd.read_csv("drinks.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Check date format
df["date"] = pd.to_datetime(
    df["date"], format="%d-%m-%Y", errors="coerce"
)

print("\nInvalid dates:")
print(df[df["date"].isnull()])

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check energy ratings
print("\nInvalid energy ratings:")
print(df[~df["energy"].between(1, 5)])

# Check taste ratings
print("\nInvalid taste ratings:")
print(df[~df["taste_rating"].between(1, 5)])

print(df)

conn = sqlite3.connect("drinks.db")

#Stop if data contains errors
if (df.isnull().any().any()
    or not df["energy"].between(1, 5).all()
    or not df["taste_rating"].between(1, 5).all()):
    print("Data validation failed!")
    exit()

print("\nData validation passed!")
    

# Save CSV data to SQLite
df.to_sql("drinks", conn, if_exists="replace", index=False) #переносить дані з pandas DataFrame у таблицю SQLite.

print("\nData saved successfully!")


# Count drinks by type
query = """
SELECT drink_type, COUNT(*) AS total
FROM drinks
GROUP BY drink_type
ORDER BY total DESC
"""

result = pd.read_sql_query(query, conn)

print("\nNumber of drinks by type:\n")
print(result)


# Average taste rating by drink type
query = """
SELECT drink_type, AVG(taste_rating) AS average_taste
FROM drinks
GROUP BY drink_type
ORDER BY average_taste DESC
"""

result = pd.read_sql_query(query, conn).round(2)

print("\n\nAverage taste rating by drink type:\n")
print(result)


# Count drinks at university
query = """
SELECT COUNT(*) AS university_drinks
FROM drinks
WHERE location = 'university'
"""

result = pd.read_sql_query(query, conn)

print("\n\nNumber of drinks at university:\n")
print(result)


# Pandas analysis, average energy by drink type
average_energy = df.groupby("drink_type")["energy"].mean().round(2)

print("\n\nAverage energy level by drink type:\n")
print(average_energy)


# Load data from SQLite into pandas
db_df = pd.read_sql("SELECT * FROM drinks", conn)

db_df["date"] = pd.to_datetime(db_df["date"]).dt.strftime("%d-%m-%Y")

print("\n\nData loaded from SQLite:\n")
print(db_df.head())


# Bar chart, number of drinks by type
drink_counts = db_df["drink_type"].value_counts()

plt.figure()
plt.bar(drink_counts.index, drink_counts.values)

plt.title("Number of Drinks by Type")
plt.xlabel("Drink Type")
plt.ylabel("Number of Drinks")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("drinks_chart.png")
plt.show()


# Bar Chart, Average Energy Level by Drink Type

average_energy = db_df.groupby("drink_type")["energy"].mean().round(2)

plt.figure()
plt.bar(average_energy.index, average_energy.values)

plt.title("Average Energy Level by Drink Type")
plt.xlabel("Drink Type")
plt.ylabel("Average Energy Level")

plt.ylim(0, 5)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("energy_chart.png")
plt.show()


# Line Chart, Average Energy Level by Date

# Convert date to datetime
db_df["date"] = pd.to_datetime(db_df["date"], format="%d-%m-%Y")

# Calculate average energy for each day
daily_energy = db_df.groupby("date")["energy"].mean().round(2)

# Create line chart
plt.figure()
plt.plot(daily_energy.index, daily_energy.values, marker="o")

plt.title("Average Energy Level by Date")
plt.xlabel("Date")
plt.ylabel("Average Energy Level")

plt.ylim(0, 5)
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("daily_energy_chart.png")
plt.show()


# Close database connection
conn.close()
