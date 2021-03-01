import psycopg2
con = psycopg2.connect(
  database="postgres",
  user="postgres",
  password="postgres",
  host="127.0.0.1",
  port="5432"
)

print("Database opened successfully")
cur = con.cursor()
cur.execute('''CREATE TABLE HISTORY_WEATHER
     (ID INT PRIMARY KEY NOT NULL,
     DATE date NOT NULL,
     Maximum_Temperature DECIMAL(5,2),
     Minimum_Temperature DECIMAL(5,2),
     Temperature DECIMAL(5,2),
     Wind_Chill REAL, 
     Heat_Index REAL, 
     Precipitation REAL,
     Snow_Depth REAL, 
     Wind_Speed REAL,
     Wind_Gust REAL,
     Visibility REAL,
     Cloud_Cover REAL,
     Relative_Humidity REAL,
     Conditions CHAR(100))''')

print("Table created successfully")
con.commit()
con.close()
f = open('Новая папка/weatherdata.csv', 'r')
cur.copy_from(f, 'HISTORY_WEATHER', sep=';')
f.close()
