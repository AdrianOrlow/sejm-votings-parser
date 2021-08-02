import requests
import json
from bs4 import BeautifulSoup

class SejmVoting:
    baseUrl = 'https://www.sejm.gov.pl/sejm9.nsf/agent.xsp?symbol=glosowania&NrKadencji=9'
    sittingIndex = ""
    votingIndex = ""

    def __init__(self, sittingIndex, votingIndex):
        self.queryUrl = self.getQueryUrl(sittingIndex, votingIndex)
        self.sittingIndex = sittingIndex
        self.votingIndex = votingIndex

    def getQueryUrl(self, sittingIndex, votingIndex):
        return f"{self.baseUrl}&NrPosiedzenia={sittingIndex}&NrGlosowania={votingIndex}"

    def getPage(self):
        response = requests.get(self.queryUrl)
        page = BeautifulSoup(response.text, 'html.parser')
        notFound = page.find(text="Brak danych")

        return None if notFound is not None else page

    def getVoting(self):
        page = self.getPage()
        if page is None:
            print(page)
            return page

        rows = page.find_all('tr')[1:]
        topic, form = page.select("p.subbig")
        data = {
            'topic': topic.text,
            'form': form.text,
            'date': page.select('#title_content > h1 > small')[0].text[5:15],
            'sitting': self.sittingIndex,
            'voting': self.votingIndex,
            'results': {},
        }
    
        for row in rows:
            cols = row.find_all('td')[:7]
            club = cols[0].text
            cols_numbers = [int(ele.text.replace("-", "0")) for ele in cols[1:]]
            members, _, _for, against, abstain, absent = cols_numbers

            data['results'][club] = {
                'members': members,
                'for': _for,
                'against': against,
                'abstain': abstain,
                'absent': absent
            }

        print(json.dumps(data, indent=4))



sv = SejmVoting(35, 8)
sv.getVoting()
