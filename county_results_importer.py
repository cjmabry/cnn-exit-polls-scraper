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
except psycopg2.Error as e:
    print('db connection failure')
    print(e)

def main():
    # for filename in os.listdir(fileDir + '/' + '2016'):
    #     print("filename = "+ filename)
    #     if filename.endswith('.json'):
    #         with open(fileDir + '/' + '2016/' + filename) as jsonData:
    #             state = json.load(jsonData)
    #             extractData2016(state)
    with open(fileDir + '/' + '2012/AZ.json') as jsonData:
        state = json.load(jsonData)
        extractData2016(state)


def BoolStringToInt(string):
    if string.lower() == 'false':
        return 0
    elif string.lower() == 'true':
        return 1


def extractData2016(stateJSON):
    print('extractData2016 begin')
    # one record in StateDataByYear
    raceDict = stateJSON['race']
    stateId = raceDict['code']
    stateName = raceDict['state']
    isKeyRace = int(raceDict['keyrace'])
    electoralVotes = raceDict['evotes']
    pollClosedTimestamp = raceDict['pollclose']
    stateCalledByCNNTimestamp = raceDict['calltime']
    percentReporting = raceDict["pctsrep"]

    cursor = pgConn.cursor()
    statement = 'INSERT into state_data_by_year \
        (state_id, state_name, year, is_key_race, electoral_votes, poll_closed_ts, state_called_by_cnn_ts, percent_reporting) \
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' 
    values = (stateId, stateName, '2016', isKeyRace, electoralVotes, pollClosedTimestamp, stateCalledByCNNTimestamp, percentReporting)
    cursor.execute(statement, values)
    # pgConn.commit()



    # many records in CandidateDataByState
    for candidate in stateJSON['race']['candidates']:
        candidateId = candidate['id']
        lastName = candidate['lname']
        party = candidate['party']
        isWinner = int(candidate['winner'])
        percentOfVote = candidate['pctDecimal']
        totalVotes = candidate['votes']
        electoralVotesWon = candidate['evotes']
        cursor = pgConn.cursor()
        statement = 'INSERT into candidate_data_by_state \
            (state_id, year, candidate_id, last_name, party, is_winner, percent_of_vote, total_votes, electoral_votes_won) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)' 
        values = (stateId, '2016', candidateId, lastName, party, isWinner, percentOfVote, totalVotes, electoralVotesWon)
        cursor.execute(statement, values)

    pgConn.commit()

    # # one record in CountyDataByYear
    # countiesDict = resultsJSON['counties']
    # cnnCountyId = countiesDict['co_id']
    # countyName = countiesDict['name']
    # updatedAtTimestamp = countiesDict['race']['ts']
    # percentReporting = countiesDict['race']['pctsrep']

    # # many records in CandidateDataByCounty
    # candidateDict = countiesDict['race']['candidates']
    # candidateId = candidateDict['id']
    # lastName = candidateDict['lname']
    # party = candidateDict['party']
    # isWinner = candidateDict['winner']
    # percentOfVote = candidateDict['pctDecimal']
    # totalVotes = candidateDict['votes']


main()



