import pyodbc
class DB:
    def __init__(self):
        self.conn = pyodbc.connect(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=localhost\SQLEXPRESS;'
            r'DATABASE=DSMP;'
            r'Trusted_Connection=yes;',
            # autocommit=True
        )

        self.cursor = self.conn.cursor()
    def fetch_cities(self):
        self.cursor.execute("""SELECT Source FROM flights
                                UNION
                                SELECT Destination FROM flights""")

        data = self.cursor.fetchall()
        cities = []
        for i in data:
            cities.append(i[0])
        return cities

    def fetch_flight_details(self,source,destination):
        self.cursor.execute(
            """SELECT Airline, Route, Dep_Time, Duration, Price
               FROM flights
               WHERE source = ? AND destination = ?
               AND Total_Stops='non-stop'
               """,
            (source, destination)
        )

        data1 = self.cursor.fetchall()
        print(data1)
        if not data1:
            return 'No Direct Flights Available'
        else:
            return data1
    def fetch_flight_details(self,source,destination,flag):
        if flag==1:
            self.cursor.execute(
                """SELECT Airline, Route, Dep_Time, Duration, Price
                    FROM flights
                    WHERE source = ? AND destination = ?
                    AND Total_Stops='non-stop'""",
            (source, destination))
        else:
            self.cursor.execute(
                """SELECT Airline, Route, Dep_Time, Duration, Price
                    FROM flights
                    WHERE source = ? AND destination = ?""",
                (source, destination))

        data1 = self.cursor.fetchall()
        # print(data1)
        if not data1:
            return 'No Direct Flights Available'
        else:
            return data1
    def fetch_airline_fre(self):
        airline=[]
        frequency=[]
        self.cursor.execute(("""
        SELECT Airline,count(*) FROM flights
        GROUP BY Airline
        """))

        data = self.cursor.fetchall()

        for i in data:
            airline.append(i[0])
            frequency.append(i[1])

        return  airline,frequency

    def busiest_airpot(self):
        airort = []
        no_of_flights = []
        self.cursor.execute(("""
                SELECT e.Station,count(*)   
                FROM
                (SELECT Source AS Station FROM flights
                UNION ALL
                SELECT Destination AS Station FROM flights
                ) AS e GROUP BY Station
                """))

        data = self.cursor.fetchall()
        for i in data:
            airort.append(i[0])
            no_of_flights.append(i[1])

        return airort, no_of_flights

    def daily_flights_airline(self):
        doj=[]
        total_flights=[]
        self.cursor.execute(("""SELECT Date_of_Journey,count(*) AS 'Total' FROM flights
                        group by Date_of_Journey
                        """))
        data = self.cursor.fetchall()
        for i in data:
            doj.append(i[0])
            total_flights.append(i[1])
        return doj,total_flights