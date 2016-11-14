import requests, json
import unicodecsv as csv
from pprint import pprint
import psycopg2

# config for primaries
party = 'Dem'
candidates = ['Clinton', 'Sanders']

# config for generals
parties = ['Dem', 'Rep']

# manually group states by region for better analysis
# http://www2.census.gov/geo/pdfs/reference/GARM/Ch6GARM.pdf
regions = {
    'South' : {
        'South Atlantic' : [
            'WV',
            'MD',
            'DE',
            'DC',
            'VA',
            'NC',
            'SC',
            'GA',
            'FL'
        ],
        'East South Central': [
            'KY',
            'TN',
            'MS',
            'AL'
        ],
        'West South Central': [
            'OK',
            'AR',
            'LA',
            'TX'
        ]
    },
    'West' : {
        'Mountain': [
            'MT',
            'ID',
            'WY',
            'NV',
            'UT',
            'CO',
            'AZ',
            'NM'
        ],
        'Pacific': [
            'AK',
            'WA',
            'OR',
            'HI'
        ]
    },
    'Midwest' : {
        'West North Central' : [
            'ND',
            'SD',
            'NE',
            'KS',
            'MN',
            'IA',
            'MO'
        ],
        'East North Central' : [
            'WI',
            'IL',
            'MI',
            'IN',
            'OH'
        ]
    },
    'Northeast' : {
        'Middle Atlantic' : [
            'PA',
            'NY',
            'NJ'
        ],
        'New England' : [
            'ME',
            'VT',
            'NH',
            'MA',
            'CT',
            'RI'
        ]
    }
}


def getCountyDataForStateAndYear(state):
    year = 2016
    # example urls
    # P_county.json = president
    # S_county.json = senate
    # http://data.cnn.com/ELECTION/2016/AZ/county/P_county.json
    # http://data.cnn.com/ELECTION/2016/NV/county/P_county.json
    print('getCountyDataForState: ' + state + ' year = ' + str(year))
    r = requests.get('http://data.cnn.com/ELECTION/' + str(year) + '/' + state + '/county/P_county.json')
    # print(r.json())
    # saveToCSV(r, state, year)

def saveToCSV(request, state, year):
    print('saveToCSV begin for state = ' + state + ' year = ' + str(year))

    state_subregion = ''
    state_region = ''
    if response.status_code == 200:
        for region, subregions in regions.iteritems():
            for subregion, states in subregions.iteritems():
                if state in states:
                    state_subregion = subregion
                    state_region = region

        filename = 'data/general/' + str(year) + '/' + state + '.csv'
        data = response.json()
        states = {}
        counties = {}

        with open(filename, 'wb') as f:
            csv_file = csv.writer(f, delimiter='\t', dialect='excel', encoding='utf-8')


def extractData(resultsJSON):
    # one record in StateDataByYear
    raceDict = resultsJSON['race']
    stateId = raceDict['code']
    stateName = raceDict['state']
    isKeyRace = raceDict['keyrace']
    electoralVotes = raceDict['evotes']
    pollClosedTimestamp = raceDict['pollclose']
    stateCalledByCNNTimestamp = raceDict['calltime']
    percentReporting = raceDict["pctsrep"]

    # many records in CandidateDataByState
    for candidate in raceDict['candidates']:
        candidateId = candidate['id']
        lastName = candidate['lname']
        party = candidate['party']
        isWinner = candidate['winner']
        percentOfVote = candidate['pctDecimal']
        totalVotes = candidate['votes']
        electoralVotesWon = candidate['evotes']

    # one record in CountyDataByYear
    countiesDict = resultsJSON['counties']
    cnnCountyId = countiesDict['co_id']
    countyName = countiesDict['name']
    updatedAtTimestamp = countiesDict['race']['ts']
    percentReporting = countiesDict['race']['pctsrep']

    # many records in CandidateDataByCounty
    candidateDict = countiesDict['race']['candidates']
    candidateId = candidateDict['id']
    lastName = candidateDict['lname']
    party = candidateDict['party']
    isWinner = candidateDict['winner']
    percentOfVote = candidateDict['pctDecimal']
    totalVotes = candidateDict['votes']






getCountyDataForStateAndYear('NV')
