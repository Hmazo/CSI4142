import psycopg2
from psycopg2 import Error
import pandas as pd

# define the database connection parameters
host = "localhost"
database = "csi4142"
user = "postgres"
password = "papi"

# establish a connection to the database
try:
    connection = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )
    print("Connected to the PostgreSQL database successfully")
except Error as e:
    print(f"Error connecting to the PostgreSQL database: {e}")

# create a cursor object
cursor = connection.cursor()
df = pd.read_csv("Country_Dimension.csv")
df =df.drop(columns=['Unnamed: 0'])
# create a table with the same name as the Pandas DataFrame
table_name = "targetcountry"
columns = ", ".join(df.columns)
create_table_query = '''
CREATE TABLE targetcountry (
    country_code text,
    country text,
    lat numeric(10, 6),
    long numeric(10, 6),
    income text,
    mean_migration_mean numeric(10, 6),
    mean_migration_median numeric(10, 6),
    average_migration_mean numeric(10, 6),
    average_migration_median numeric(10, 6),
    surrogate_keys integer
);
'''

cursor.execute(create_table_query)
print(f"Table '{table_name}' created successfully")

# insert the data from the Pandas DataFrame into the PostgreSQL table
for row in df.itertuples(index=False):
    values = tuple(row)
    placeholders = ", ".join(["%s"] * len(row))
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"
    cursor.execute(insert_query, values)
connection.commit()
print(f"{len(df)} rows inserted into '{table_name}' table")

# close the database connection
cursor.close()
connection.close()
print("PostgreSQL connection is closed")
