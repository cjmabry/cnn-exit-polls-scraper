import scrapy, json, csv, pprint

class ExitPollSpider(scrapy.Spider):
  name = 'exitPollsSpider'
  start_urls = ['http://data.cnn.com/ELECTION/2016primary/AR/xpoll/Dfull.json']

  def parse(self, response):
    filename = response.url.split("/")[-3] + '.csv'
    data = json.loads(response.body)

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

                csv_file.writerow(['',answer['answer'],answer['pct'],d[item['question']][answer['answer']]['Clinton'],d[item['question']][answer['answer']]['Sanders']])

    pprint.pprint(d)
