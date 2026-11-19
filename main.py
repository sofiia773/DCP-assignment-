import pandas as pd
import sqlite3

df = pd.read_csv("drinks.csv")

# Remove extra spaces from column names
df.columns = df.columns.str.strip()

# Check date format
df["date"] = pd.to_datetime(
    df["date"], format="%d-%m-%Y", errors="coerce"
)

print("Invalid dates:")
print(df[df["date"].isnull()])

# Check for missing values
print("Missing values:")
print(df.isnull().sum())

# Check energy ratings
print("Invalid energy ratings:")
print(df[~df["energy"].between(1, 5)])

# Check taste ratings
print("Invalid taste ratings:")
print(df[~df["taste_rating"].between(1, 5)])

print(df)

conn = sqlite3.connect("drinks.db")

#Stop if data contains errors
if (df.isnull().any().any()
    or not df["energy"].between(1, 5).all()
    or not df["taste_rating"].between(1, 5).all()):
    print("Data validation failed!")
    exit()

print("Data validation passed!")
    

# Save CSV data to SQLite
df.to_sql("drinks", conn, if_exists="replace", index=False) #переносить дані з pandas DataFrame у таблицю SQLite.

print("Data saved successfully!")


# Count drinks by type
query = """
SELECT drink_type, COUNT(*) AS total
FROM drinks
GROUP BY drink_type
ORDER BY total DESC
"""

result = pd.read_sql_query(query, conn)

print("Number of drinks by type:")
print(result)


# Average taste rating by drink type
query = """
SELECT drink_type, AVG(taste_rating) AS average_taste
FROM drinks
GROUP BY drink_type
ORDER BY average_taste DESC
"""

result = pd.read_sql_query(query, conn)

print("Average taste rating by drink type:")
print(result)


# Count drinks at university
query = """
SELECT COUNT(*) AS university_drinks
FROM drinks
WHERE location = 'university'
"""

result = pd.read_sql_query(query, conn)

print("Number of drinks at university:")
print(result)

# Close database connection
conn.close()
