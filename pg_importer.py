import psycopg2
import os
import csv



def main():

    fileDir = './data/general'
    
    pgParams = {
        'dbname': 'abannin',
        'user': 'abannin',
        'password': ''
    }

    try:
        pgConn = psycopg2.connect(**pgParams)
        print('db connection successful')
    except psycopg2.Error as e:
        print('db connection failure')
        print(e)
        return
        
    for year in ['2012', '2016']:
        for filename in os.listdir(fileDir + '/' + year):

            if filename.endswith('.csv'):
                # first import file into temp table
                print("filename: " + fileDir + '/' + year + '/' + filename)
                cursor = pgConn.cursor()
                cursor.execute("delete from temp;")
                importFile = open(fileDir + '/' + year + '/' + filename, "r+")
                cursor.copy_from(importFile, 'temp', sep = '\t', null="")
                pgConn.commit()

                # merge temp table into primary table
                # cursor.execute("delete from exit_polls where year = " + year + " and state = " + state + ";")
                # cursor.execute("insert into exit_polls select * from temp;")



main()