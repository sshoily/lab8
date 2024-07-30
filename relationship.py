"""
Description:
 Creates the connections table in the Social Network database
 and populates it with 100 random connections.

Usage:
 python create_connections.py
"""
import os
import sqlite3
from faker import Faker

# Determine the path of the database
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'social_network.db')

def main():
    create_connections_table()
    populate_connections_table()

def create_connections_table():
    """Creates the connections table in the DB"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # SQL command to create the connections table
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS connections (
        connection_id INTEGER PRIMARY KEY,
        individual1_id INTEGER NOT NULL,
        individual2_id INTEGER NOT NULL,
        connection_type TEXT NOT NULL,
        initiation_date TEXT NOT NULL,
        FOREIGN KEY (individual1_id) REFERENCES individuals (id),
        FOREIGN KEY (individual2_id) REFERENCES individuals (id)
    );
    """
    
    cur.execute(create_table_sql)
    con.commit()
    con.close()

def populate_connections_table():
    """Adds 100 random connections to the DB"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    faker = Faker()
    
    # Insert 100 random connections
    for _ in range(100):
        individual1_id = faker.random_int(min=1, max=100)  # Assuming there are 100 individuals
        individual2_id = faker.random_int(min=1, max=100)
        connection_type = faker.random_element(elements=('friendship', 'family', 'coworker', 'spouse'))
        initiation_date = faker.date_between(start_date='-10y', end_date='today')
        
        # Ensure individual1_id and individual2_id are not the same
        while individual1_id == individual2_id:
            individual2_id = faker.random_int(min=1, max=100)
        
        cur.execute("INSERT INTO connections (individual1_id, individual2_id, connection_type, initiation_date) VALUES (?, ?, ?, ?)",
                    (individual1_id, individual2_id, connection_type, initiation_date))
    
    con.commit()
    con.close()

if __name__ == '__main__':
   main()
