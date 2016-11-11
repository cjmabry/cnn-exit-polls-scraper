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
                pgConn.commit()
                importFile = open(fileDir + '/' + year + '/' + filename, "r+")
                cursor.copy_from(importFile, 'temp', sep = '\t', null="")
                pgConn.commit()

                # merge temp table into primary table
                state = filename.split('.')[0]
                cursor.execute("delete from exit_polls where year = " + str(year) + " and state = '''" + state + "''';")
                pgConn.commit()
                # select * from temp where state = 'AL' and year = '2012
                cursor.execute("insert into exit_polls select * from temp;")
                pgConn.commit()



main()