#!/usr/bin/env python3

import sqlite3 as s3
from sqlite3 import Error
import os
from os import getenv
import sys
import requests
import json

DB_NAME = 'db.sqlite3'

# Find matches between client data and Neanderthal variant data
COMPARE_TABLES_SQL = """
    SELECT C.accession_id, C.start, C.end, C.allele, C.dosage
    FROM client_data C
    INNER JOIN neanderthal_variants N
    ON C.start = N.start
    AND C.end = N.end
    AND C.allele = N.neanderthal_allele
"""

# Max returned for each accession_id. Lower reduces program run time; higher increases program accuracy.
LIMIT = '5000'

# Using 23andMe demo data
HEADERS = {
    'Authorization': 'Bearer demo_oauth_token'
}


# Create database connection and run welcome message
def setup():
    conn = create_connection(DB_NAME)
    if conn is not None:
        os.system('cls' if os.name == 'nt' else 'clear')
        welcome_message(conn)
    else:
        print("Error! Cannot create the database connection.")

def create_connection(db_file):
    try:
        conn = s3.connect(db_file)
        return conn
    except s3.Error as e:
        print(e)
    return conn

def welcome_message(conn):
    print('\n**********************************\n')
    print('23andMe Neanderthal Variant Demo\n')
    print('**********************************\n')
    print('Welcome! Thank you for your patience as we download genetic data')
    print('for 22 accession ids containing potential Neanderthal variants.\n')
    
    get_neanderthal_accessions(conn)



# Obtain all Neanderthal-related accession ids from database
def get_neanderthal_accessions(conn):
    csr = conn.cursor()
    csr.execute("SELECT * FROM neanderthal_accessions")
    rows = csr.fetchall()
    for row in rows:
        get_client_data(conn, row[0])

    find_variant_matches(conn)


# Obtain potential Neanderthal variants from client data based on accession ids
def get_client_data(conn, accession_id):
    print('Downloading data for ' + accession_id + '...')

    response = requests.get(
        'https://api.23andme.com/3/profile/demo_profile_id/marker/?accession_id=' + accession_id + '&limit=' + LIMIT + ' &start=87760', headers=HEADERS)

    accession_data = response.json()['data']

    # TO DO: Utilize the "next" field to call data in batches to completion.
    # Asynchronously run data processing functions while API calls continue.
    # next = response.json()['links']['next']

    store_client_data(conn, accession_data, accession_id)


# Store client data for comparison to known Neanderthal variants
def store_client_data(conn, data, id):
    csr = conn.cursor()

    for item in data:
        current = item['variants'][0]
        dosage = current['dosage']

        if dosage:
            start = current['start']
            end = current['end']
            allele = current['allele']
            params = (id, start, end, allele, dosage)
            csr.execute(
                "INSERT INTO client_data VALUES (?, ?, ?, ?, ?)", params)
            conn.commit()


# Compare client data to Neanderthal variants
def find_variant_matches(conn):
    csr = conn.cursor()
    csr.execute(COMPARE_TABLES_SQL)
    rows = csr.fetchall()

    total_variants = 0

    print('**********************************\n')

    for row in rows:
        total_variants += row[4]

    print(total_variants, 'Neanderthal variants found.\n')
    print('**********************************')

    close_connection(conn)


# Delete client data and close connection
def close_connection(conn):
    csr = conn.cursor()
    csr.execute("DELETE FROM client_data")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "interview.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
    setup()