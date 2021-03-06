import unittest
from urllib import request

from scrape import Scraper, URL_TOPIC_LIST


class ServerTests(unittest.TestCase):
    """tests to ensure pages at dodsbir.net can be reached and lists and topics
    can be retrieved"""

    def setUp(self):
        self.s = Scraper()

    def testServerResponse(self):
        self.assertTrue(request.urlopen(URL_TOPIC_LIST))

    def testStageSolicitation(self):
        self.assertFalse(self.s.topic_ids)
        self.s.stage_current_solicitation()
        self.assertTrue(self.s.topic_ids)


class TopicTests(unittest.TestCase):
    """tests to ensure Topics are successfully scraped and stored in the proper
    format"""

    def setUp(self):
        self.s = Scraper()

    def testTopicRetrieved(self):
        self.assertFalse(hasattr(self, "topic"))
        topic = self.s.get_topic("SB151-004")
        self.assertTrue(topic)

    def testTopicSolicitationID(self):
        topic = self.s.get_topic("SB151-004")
        self.assertEqual(topic.solicitation_id, "DoD SBIR 2015.1")

    def testDatesConvertedToPythonObject(self):
        topic = self.s.get_topic("SB151-004")
        self.assertTrue(topic.pre_release_date.month)
        self.assertTrue(topic.proposals_begin_date.month)
        self.assertTrue(topic.proposals_end_date.month)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
