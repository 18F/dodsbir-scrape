from bs4 import BeautifulSoup
import mechanize
import re
import time
import urllib

from dodsbirtopic import DODSBIRTopic

URL_RESULTS_FORM = "http://dodsbir.net/Topics/BasicTopicsResultsForm.asp"
URL_TOPIC_LIST = "http://dodsbir.net/Topics/Default.asp"
URL_TOPIC_BASE = "http://www.dodsbir.net/sitis/display_topic.asp?Bookmark"

class DODSBIRScrape:
    """base class for DOD SBIR Importing"""
    def __init__(self, 
        topic_list_url=URL_TOPIC_LIST):
        self.topic_list_url = topic_list_url
        self.topic_ids = {}
        self.topics = []

    def get_topic_list(self):
        """go to topic_list_url and extract list of topics"""
        browser = mechanize.Browser()
        browser.open("%s" % self.topic_list_url)
        soup = BeautifulSoup(browser.response().read())
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
        #topic.dates = soup.find(re.compile("Proposals Accepted"))
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
        self.get_topic_list()
        topic_id = self.topic_ids[topic_number]
        data = {"selTopic":topic_id, "WhereFrom":"basicTopicNo"}
        req = mechanize.Request(URL_RESULTS_FORM, urllib.urlencode(data))
        resp = mechanize.urlopen(req)
        return self.html_to_topic(resp.read(), topic_id)

    def get_all_topics(self):
        """loop through each topic id in topic_ids and scrape topic from dodsbir.net"""
        for key, value in self.topic_ids.iteritems():
            self.topic_list = []
            topic = self.get_topic(key)
            self.topics.append(topic)
            time.sleep(1)
