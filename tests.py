import unittest
import urllib

import dodsbirscrape


class ServerTests(unittest.TestCase):
	"""tests to ensure pages at dodsbir.net can be reached and lists and topics
	can be retrieved"""

	def testServerResponse(self):
		self.assertTrue(urllib.urlopen(dodsbirscrape.URL_TOPIC_LIST))

	def testTopicListRetrieved(self):
		s = dodsbirscrape.DODSBIRScrape()
		self.assertFalse(s.topic_ids)
		s.get_topic_list()
		self.assertTrue(s.topic_ids)

	def testTopicRetrieved(self):
		s = dodsbirscrape.DODSBIRScrape()
		topic = s.get_topic("SB142-004")
		self.assertTrue(topic.title)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
