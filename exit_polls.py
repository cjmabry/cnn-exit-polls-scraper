import requests, csv, json
from pprint import pprint

party = 'Dem'
candidates = ['Clinton', 'Sanders']
# party = 'Rep'
# candidates = ['Trump', 'Cruz', 'Kasich']


r = requests.get('http://data.cnn.com/elections/2016/config.json')

data = r.json()

exitpollhub = data['data']['exitpollhub']

for poll in exitpollhub:
    if party == 'Dem':
        urls = ['Dfull','Efull'] # IA and NV use Efull
    elif party == 'Rep':
        urls = ['Rfull','Sfull'] # IA and NV use Sfull

    for url in urls:
        r = requests.get('http://data.cnn.com/ELECTION/2016primary/' + poll['statecode'] + '/xpoll/'+ url + '.json')

        if r.status_code == 200:

            if poll['party'] == party:
                filename = 'data/' + party + '/' + poll['statecode'] + '-' + party +'.csv'
                data = r.json()
                d = {}

                with open(filename, 'wb') as f:
                    csv_file = csv.writer(f)
                    csv_file.writerow(['Question','Answer','Percentage of Electorate','Clinton','Sanders'])

                    for item in data['polls']:
                        csv_file.writerow([item['question']])

                        # dictionary for debugging
                        d[item['question']] = {}

                        for answer in item['answers']:

                            # dictionary for debugging
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

                            csv_file.writerow(['',answer['answer'],answer['pct'],d[item['question']][answer['answer']][candidates[0]],d[item['question']][answer['answer']][candidates[1]]])
