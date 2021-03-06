import requests, csv, json
from pprint import pprint

party = 'Dem'
candidates = ['Clinton', 'Sanders']

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

r = requests.get('http://data.cnn.com/elections/2016/config.json')

data = r.json()

exitpollhub = data['data']['exitpollhub']

for poll in exitpollhub:
    if party == 'Dem':
        urls = ['Dfull','Efull'] # IA and NV use Efull
    elif party == 'Rep':
        urls = ['Rfull','Sfull'] # IA and NV use Sfull

    state = poll['statecode']


    for url in urls:
        r = requests.get('http://data.cnn.com/ELECTION/2016primary/' + state + '/xpoll/'+ url + '.json')

        if r.status_code == 200:
            for region, subregions in regions.items():
                for subregion, states in subregions.items():
                    if state in states:
                        state_subregion = subregion
                        state_region = region

            if poll['party'] == party:
                filename = 'data/' + party + '/' + state + '-' + party +'.csv'
                data = r.json()
                d = {}

                with open(filename, 'w') as f:
                    csv_file = csv.writer(f)
                    csv_file.writerow(['question','pollname','state','region','subregion','answer','percent','clinton','sanders'])

                    for item in data['polls']:

                        d[item['question']] = {}

                        for answer in item['answers']:

                            d[item['question']][answer['answer']] = {}
                            d[item['question']][answer['answer']]['Percent of Electorate'] = answer['pct']

                            results = {}

                            for a in answer['candidateanswers']:
                                if a['id'] == 1746:
                                    candidate = 'Clinton'
                                elif a['id'] == 1445:
                                    candidate = 'Sanders'
                                else:
                                    candidate = None

                                d[item['question']][answer['answer']][candidate] = a['pct']

                            csv_file.writerow([item['question'],item['pollname'],state,state_region,state_subregion,answer['answer'],answer['pct'],d[item['question']][answer['answer']][candidates[0]],d[item['question']][answer['answer']][candidates[1]]])
