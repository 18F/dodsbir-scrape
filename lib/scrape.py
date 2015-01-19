from datetime import datetime
import json, re, sys, time

from bs4 import BeautifulSoup
import requests

from dodsbir.topic import Topic, TopicEncoder

URL_RESULTS_FORM = "http://dodsbir.net/Topics/BasicTopicsResultsForm.asp"
URL_TOPIC_LIST = "http://dodsbir.net/Topics/Default.asp"
URL_TOPIC_BASE = "http://www.dodsbir.net/sitis/display_topic.asp?Bookmark"
URL_TOPIC_QUICK = "http://www.dodsbir.net/sitis/quick_scan.asp"
URL_SOLICITATION_SCHED = "http://www.acq.osd.mil/osbp/sbir/sb/schedule.shtml"


class Scraper:
    """base class for DOD SBIR Scraping"""
    def __init__(self, topic_list_url=URL_TOPIC_LIST):
        self.solicitation = {}
        self.solicitation_schedule = [] # this will contain nested dicts
        self.topic_list_url = topic_list_url
        self.topic_ids = {}
        self.topics = []

    def get_solicitation(self, soup):
        """extract solicitation information from page at URL_TOPIC_LIST"""
        sol_header = soup.find(text=re.compile("Current Solicitation"))

        s = {}
        # maybe change solicitation_id to pull from
        # http://www.dodsbir.net/sitis/quick_scan.asp -- seems to be more accurate
        sol_id_raw = sol_header.parent.parent.next_sibling\
            .next_sibling.contents[1].string
        try:
            s["solicitation_id"] = re.search(r'\d{4}\.[1-2A-B]', sol_id_raw).group()
        except Exception as e:
            s["solicitation_id"] = sol_id_raw

        s["pre_release_date"] = self._parse_date(sol_header.parent.parent.next_sibling.next_sibling.contents[3].string)
        s["proposals_begin_date"] = self._parse_date(sol_header.parent.parent.next_sibling.next_sibling.contents[5].string)
        s["proposals_end_date"] = self._parse_date(sol_header.parent.parent.next_sibling.next_sibling.contents[7].contents[0].string)
        agencies = sol_header.parent.parent.next_sibling.next_sibling.contents[9].string.split(',')
        s["participating_components"] = [ x.strip() for x in agencies ]
        return s

    def stage_current_solicitation(self):
        """gets information for current solicitation and grabs list of topics
        for the current solicitation"""
        resp = requests.get(self.topic_list_url)
        resp.connection.close()  # fixes warning in Python 3.4 about unclosed socket
        soup = BeautifulSoup(resp.text)
        self.solicitation = self.get_solicitation(soup)
        self.topic_ids = self.get_topic_list(soup)
        return True

    def get_topic_list(self, soup):
        """go to topic_list_url and extract list of topics"""
        self.topic_ids = {}
        options = soup.find_all('select')[0].find_all('option')
        for option in options:
            if option.string.strip() != '':
                self.topic_ids[option.string.strip()] = option['value']
        return self.topic_ids

    def html_to_topic(self, html, topic_id):
        """extract topic information from html"""
        soup = BeautifulSoup(html)
        meta_rows = soup.findAll('table')[1].contents
        rows = soup.findAll('table')[2].contents

        topic = Topic()
        topic.program = meta_rows[1].findAll('td')[1].contents[0].string
        topic.topic_number = meta_rows[2].findAll('td')[1].contents[0].string
        topic.title = meta_rows[3].findAll('td')[1].contents[0].string
        topic.areas = [ x.strip() for x in meta_rows[4].findAll('td')[1]\
            .contents[0].string.split(',') ]
        topic.url = "%s=%s" % (URL_TOPIC_BASE, topic_id)

        acq_header = soup.find(text=re.compile("Acquisition Program:"))
        if acq_header is not None:
            acq_field = acq_header.parent.parent.parent.next_sibling\
                .contents[0].string
            if acq_field is not None:
                topic.acquisition_program = acq_field.strip()

        obj_header = soup.find(text=re.compile("Objective:"))
        topic.objective = obj_header.parent.parent.parent.next_sibling\
            .contents[0].string.strip()

        desc_header = soup.find(text=re.compile("Description:"))
        topic.description = desc_header.parent.parent.parent.next_sibling\
            .contents[0].string.strip()

        topic.phases = [p.strip() for p in soup\
            .find_all(text=re.compile("^PHASE"))]

        ref_header = soup.find(text=re.compile("References:"))
        topic.references = [reference.strip() \
            for reference in ref_header.parent.parent.parent.next_sibling\
                .contents[0].find_all(text=re.compile("\n\d."))]

        kw_header = soup.find(text=re.compile("^Keywords:"))
        try:
            topic.keywords = [keyword.strip() for keyword in kw_header.parent\
                .parent.parent.next_sibling.contents[0].string.strip()\
                .rstrip('.').split(',')]
        except:
            topic.keywords = []

        return topic

    def get_topic(self, topic_number):
        """given a topic number, fetch topic page from dodsbir.net"""
        if not self.solicitation:
            self.stage_current_solicitation()
        topic_id = self.topic_ids[topic_number]
        data = {"selTopic":topic_id, "WhereFrom":"basicTopicNo"}
        resp = requests.post(URL_RESULTS_FORM, data=data)
        resp.connection.close()  # fixes py3 warning
        topic = self.html_to_topic(resp.text, topic_id)
        topic.solicitation_id = "DoD {} {}".format(topic.program, self.solicitation['solicitation_id'])
        topic.pre_release_date = self.solicitation['pre_release_date']
        topic.proposals_begin_date = self.solicitation['proposals_begin_date']
        topic.proposals_end_date = self.solicitation['proposals_end_date']
        topic.participating_components = self.solicitation['participating_components']
        return topic

    def get_all_topics(self, max=None):
        """loop through each topic id in topic_ids and scrape topic from 
        dodsbir.net"""
        i = 0
        tot = len(self.topic_ids)
        for key, value in self.topic_ids.items():
            i = i + 1
            self.topic_list = []
            topic = self.get_topic(key)
            self.topics.append(topic)
            sys.stdout.write("Completed %d of %d \r" % (i, tot))
            sys.stdout.flush()
            if i == max:
                break
            time.sleep(1)
        return self.topics

    def __json__(self):
        """json representation of all topics scraped"""
        j = "[%s]" % (",".join([json.dumps(t.__dict__, cls=TopicEncoder) for t in self.topics]))
        return j

    def save_as_json(self, path="alltopics.json"):
        """save json representation of all topics to filesystem"""
        with open(path, "w") as outfile:
            outfile.write(self.__json__())

        return self.__json__()

    def _parse_date(self, string):
        return datetime.strptime(string, "%B %d, %Y")
