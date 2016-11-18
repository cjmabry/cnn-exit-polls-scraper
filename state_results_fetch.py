import requests, json
import unicodecsv as csv
from pprint import pprint

years = [2012, 2016]

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
            'NM',
            'CA'
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

def main():
    for region, subregions in regions.iteritems():
        for subregion, states in subregions.iteritems():
            for state in states:
                getCountyDataForStateAndYear(state, 2012)
                getCountyDataForStateAndYear(state, 2016)

def getCountyDataForStateAndYear(state, year):
    # example urls
    # http://data.cnn.com/ELECTION/2016/AR/state/AR.json
    # http://data.cnn.com/ELECTION/2012/AR/state/AR.json


    print('getCountyDataForState: ' + state + ' year = ' + str(year))
    r = requests.get('http://data.cnn.com/ELECTION/' + str(year) + '/' + state + '/state/' + state + '.json')

    filename = 'data/states/' + str(year) + '/' + state + '.json'
    with open(filename, 'wb') as f:
        json.dump(r.json(), f)

main()
# getCountyDataForStateAndYear('NV', 2012)
