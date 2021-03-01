import psycopg2
con = psycopg2.connect(
  database="weather_data",
  user="postgres",
  password="postgres",
  host="127.0.0.1",
  port="5432"
)

print("Database opened successfully")
cur = con.cursor()
cur.execute('''CREATE TABLE weather_data
(address varchar(256) DEFAULT NULL,
   latitude   real DEFAULT NULL,
   longitude   real DEFAULT NULL,
   datetime  date DEFAULT NULL,
   maxt   real DEFAULT NULL,
   mint   real DEFAULT NULL,
   temp   real DEFAULT NULL,
   precip   real DEFAULT NULL,
   wspd   real DEFAULT NULL,
   wdir   real DEFAULT NULL,
   wgust   real DEFAULT NULL,
   pressure   real DEFAULT NULL)
''')

print("Table created successfully")
con.commit()
con.close()
