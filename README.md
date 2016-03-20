# CNN 2016 Exit Polls Scraper
Gather exit polls from CNN for the 2016 primaries and export them as state CSVs.

## Setup
* `git clone https://github.com/cjmabry/cnn-exit-polls-scraper.git`
* (optional) create virtualenv: `vitrualenv venv`
* (optional) activate it: `source venv/bin/activate`
* install dependencies:`pip install -r requirements.txt`
* run it: `python exit_polls.py`

Right now this gathers Democratic results for Clinton and Sanders. You'll have to change the party, candidates, and some logic to make it work with others. Hopefully I will make this a little less brittle in the future.
