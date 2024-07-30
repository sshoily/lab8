"""
Description:
 Generates a CSV report containing all married couples in
 the Social Network database.

Usage:
 python married_couples_report.py
"""
import os
import sqlite3
import csv
from create_connections import db_path, script_dir

def main():
    # Query DB for list of married couples
    married_couples = fetch_married_couples()

    # Save all married couples to CSV file
    csv_path = os.path.join(script_dir, 'married_couples_report.csv')
    save_married_couples_to_csv(married_couples, csv_path)

def fetch_married_couples():
    """Queries the Social Network database for all married couples.

    Returns:
        list: (name1, name2, initiation_date) of married couples 
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    query = """
    SELECT ind1.name, ind2.name, c.initiation_date
    FROM connections c
    JOIN individuals ind1 ON c.individual1_id = ind1.id
    JOIN individuals ind2 ON c.individual2_id = ind2.id
    WHERE c.connection_type = 'spouse';
    """
    
    cur.execute(query)
    married_couples = cur.fetchall()
    con.close()
    
    return married_couples

def save_married_couples_to_csv(married_couples, csv_path):
    """Saves list of married couples to a CSV file, including both people's 
    names and their wedding anniversary date  

    Args:
        married_couples (list): (name1, name2, initiation_date) of married couples
        csv_path (str): Path of CSV file
    """
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name 1', 'Name 2', 'Anniversary Date'])
        writer.writerows(married_couples)

if __name__ == '__main__':
   main()
