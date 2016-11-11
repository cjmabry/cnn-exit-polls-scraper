import psycopg2
import os


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
            copyIntoPG(filename)
            
            
        
def copyIntoPG(csvFile):
    print('copyIntoPG begin fileName: ' + csvFile)


main()