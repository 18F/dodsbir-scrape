from datetime import datetime
import json, re, sys, time

from bs4 import BeautifulSoup
import requests

from dodsbirtopic import DODSBIRTopic, TopicEncoder

URL_RESULTS_FORM = "http://dodsbir.net/Topics/BasicTopicsResultsForm.asp"
URL_TOPIC_LIST = "http://dodsbir.net/Topics/Default.asp"
URL_TOPIC_BASE = "http://www.dodsbir.net/sitis/display_topic.asp?Bookmark"


class DODSBIRScrape:
    """base class for DOD SBIR Importing"""
    def __init__(self, 
        topic_list_url=URL_TOPIC_LIST):
        self.solicitation = {}
        self.topic_list_url = topic_list_url
        self.topic_ids = {}
        self.topics = []

    def get_solicitation(self, soup):
        """extract solicitation information from page at topic_list_url"""
        sol_header = soup.find(text=re.compile("Current Solicitation"))

        s = {}
        s["solicitation_id"] = sol_header.parent.parent.next_sibling\
            .next_sibling.contents[1].string
        s["pre_release_date"] = datetime.strptime(sol_header.parent.parent\
            .next_sibling.next_sibling.contents[3].string, "%B %d, %Y")
        s["proposals_begin_date"] = datetime.strptime(sol_header.parent.parent\
            .next_sibling.next_sibling.contents[5].string, "%B %d, %Y")
        s["proposals_end_date"] = datetime.strptime(sol_header.parent.parent\
            .next_sibling.next_sibling.contents[7].contents[0].string,
            "%B %d, %Y")
        s["participating_components"] = sol_header.parent.parent.next_sibling\
            .next_sibling.contents[9].string.split(',')
        return s

    def stage_current_solicitation(self):
        """gets information for current solicitation and grabs list of topics
        for the current solicitation"""
        resp = requests.get(self.topic_list_url)
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

        topic = DODSBIRTopic()
        topic.program = meta_rows[1].findAll('td')[1].contents[0].string
        topic.topic_number = meta_rows[2].findAll('td')[1].contents[0].string
        topic.title = meta_rows[3].findAll('td')[1].contents[0].string
        topic.areas = meta_rows[4].findAll('td')[1]\
            .contents[0].string.split(',')
        topic.url = "%s=%s" % (URL_TOPIC_BASE, topic_id)
        topic.acquisition_program = rows[0].findAll('td')[1].contents[0].string

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
        topic = self.html_to_topic(resp.text, topic_id)
        topic.solicitation_id = self.solicitation['solicitation_id']
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
        for key, value in self.topic_ids.iteritems():
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
        outfile = open(path, "w")
        outfile.write(self.__json__())
        outfile.close()
        return self.__json__()
