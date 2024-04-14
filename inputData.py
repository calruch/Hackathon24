## Author: Calvin Ruch - 4/13/24
## Description: This class is used to insert data into the database
##              and fetch data from the database

import sqlite3
class Weather:
    def __init__(self, db_file):
        if db_file is None:
            raise IllegalArgumentException("Data cannot be null")
        self.db_file = db_file
        self.conn = self._connect_db(db_file)
        self._create_table(self.conn)
        self._conn_close(self.conn)

    def _connect_db(self, db_file):
        """ Connect to SQLite database """
        conn = sqlite3.connect(db_file)
        return conn

    def _table_exists(self, conn):
        """ Check if the weather table exists """
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather'")
        return bool(cursor.fetchone())

    def _create_table(self, conn):
        """ Create a table if not exists """
        if not self._table_exists(conn):
            cursor = conn.cursor()
            sql = '''
            CREATE TABLE weather(
            id INTEGER PRIMARY KEY,
            city TEXT NOT NULL,
            State TEXT NOT NULL,
            weather TEXT NOT NULL,
            time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
            '''
            cursor.execute(sql)
            conn.commit()
    def _create_table(self, conn):
        if not self._table_exists(conn):
            cursor = conn.cursor()
            sql = '''
            CREATE TABLE weather(
            id INTEGER PRIMARY KEY,
            city TEXT NOT NULL,
            State TEXT NOT NULL,
            weather TEXT NOT NULL,
            time DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
            );
            '''
            cursor.execute(sql)
            conn.commit()

            # Create a trigger to prevent duplicates within the same hour
            sql_trigger = '''
            CREATE TRIGGER prevent_duplicates
            BEFORE INSERT ON weather
            BEGIN
                SELECT CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM weather
                        WHERE city = NEW.city
                        AND State = NEW.State
                        AND weather = NEW.weather
                        AND strftime('%Y-%m-%d %H', time) = strftime('%Y-%m-%d %H', NEW.time)
                    ) THEN RAISE (ABORT, 'Duplicate record within the same hour')
                END;
            END;
            '''
            cursor.execute(sql_trigger)
            conn.commit()

    def insertData(self, data):
        conn = self._connect_db(self.db_file)
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO weather (city, State, weather) VALUES (?, ?, ?)', (data['city'], data['state'], data['weather']))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Nothing was added due to a duplicate record within the same hour.")
        finally:
            self._conn_close(conn)

    def deleteData(self): #for testing
        """ Delete data from the database """
        conn = self._connect_db(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM weather')
        conn.commit()
        self._conn_close(conn)

    def getData(self):
        """ Fetch and print all rows from the api_data table """
        conn = self._connect_db(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM weather')
        rows = cursor.fetchall()
        output = ""
        for row in rows:
            output += f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}\n"
        return output
            

    def _conn_close(self, conn):
        """ Close the connection """
        conn.close()

