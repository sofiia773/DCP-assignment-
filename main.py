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

# Close database connection
conn.close()
