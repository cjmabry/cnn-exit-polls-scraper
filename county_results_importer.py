import os
import psycopg2
import json


fileDir = './data/counties'

pgParams = {
    'dbname': 'abannin',
    'user': 'abannin',
    'password': ''
}

try:
    pgConn = psycopg2.connect(**pgParams)
    print('db connection successful')
    cursor = pgConn.cursor()
except psycopg2.Error as e:
    print('db connection failure')
    print(e)

def main():
    for year in ['2012', '2016']:
        for filename in os.listdir(fileDir + '/' + year):
            print("filename = "+ filename + " year = " + year)
            if filename.endswith('.json'):
                with open(fileDir + '/' + year + '/' + filename) as jsonData:
                    state = json.load(jsonData)
                    ImportIntoPG(state, year)
    # with open(fileDir + '/' + '2012/AZ.json') as jsonData:
    #     state = json.load(jsonData)
    #     ImportIntoPG(state, year)


def ImportIntoPG(stateJSON, year):
    print('ImportIntoPG begin')

    stateName = stateJSON['race']['state']

    for county in stateJSON['counties']:
        countyId = county['co_id']
        countyName = county['name']
        updatedAtTimestamp = county['race']["ts"]
        for candidate in county['race']['candidates']:
            candidateId = candidate['id']
            lastName = candidate['lname']
            party = candidate['party']
            isWinner = int(candidate['winner'])
            percentOfVote = candidate['vpct']
            totalVotes = candidate['votes']

            statement = 'INSERT into candidate_data_by_county \
                (state_name, year, county_id, county_name, updated_at_ts, candidate_id, last_name, party, is_winner, percent_of_vote, total_votes) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' 
            values = (stateName, year, countyId, countyName, updatedAtTimestamp, candidateId, lastName, party, isWinner, percentOfVote, totalVotes)
            cursor.execute(statement, values)

            pgConn.commit()

main()



