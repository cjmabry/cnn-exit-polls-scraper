import os
import psycopg2
import json


fileDir = './data/states'

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
            print("filename = "+ filename)
            if filename.endswith('.json'):
                with open(fileDir + '/' + year + '/' + filename) as jsonData:
                    state = json.load(jsonData)
                    ImportIntoPG(state, year)
    # with open(fileDir + '/' + '2012/AZ.json') as jsonData:
    #     state = json.load(jsonData)
    #     ImportIntoPG(state, '2012')


def BoolStringToInt(string):
    if string.lower() == 'false':
        return 0
    elif string.lower() == 'true':
        return 1


def ImportIntoPG(stateJSON, year):
    print('ImportIntoPG begin')
    
    stateId = stateJSON['code']
    stateName = stateJSON['state']
    # year = '2012'
    electoralVotes = stateJSON['evotes']
    raceDict = stateJSON['races']['P'][0]
    isKeyRace = int(raceDict['keyrace'])
    pollClosedTimestamp = raceDict['pollclose']
    updatedAtTimestamp = raceDict['ts']

    statement = 'INSERT into state_data_by_year \
        (state_id, state_name, year, is_key_race, electoral_votes, poll_closed_ts, updated_at_ts) \
        VALUES (%s, %s, %s, %s, %s, %s, %s)' 
    values = (stateId, stateName, year, isKeyRace, electoralVotes, pollClosedTimestamp, updatedAtTimestamp)
    cursor.execute(statement, values)
    # pgConn.commit()

    for candidate in raceDict['candidates']:
        # stateId
        # year
        candidateId = candidate['id']
        lastName = candidate['lname']
        party = candidate['party']
        isWinner = int(candidate['winner'])
        percentOfVote = candidate['vpct']
        totalVotes = candidate['votes']
        electoralVotesWon = candidate['evotes']

        statement = 'INSERT into candidate_data_by_state \
            (state_id, year, candidate_id, last_name, party, is_winner, percent_of_vote, total_votes, electoral_votes_won) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)' 
        values = (stateId, year, candidateId, lastName, party, isWinner, percentOfVote, totalVotes, electoralVotesWon)
        cursor.execute(statement, values)

    pgConn.commit()


main()



