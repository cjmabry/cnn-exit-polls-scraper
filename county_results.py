import requests, json
import unicodecsv as csv
from pprint import pprint

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
    # example urls
    # http://data.cnn.com/ELECTION/2016/AZ/county/P_county.json
    print('getCountyDataForState: ' + state + ' year = ' + str(year))
    r = requests.get('http://data.cnn.com/ELECTION/' + str(year) + '/' + state + '/xpoll/Pfull.json')
    saveToCSV(r, state, year)