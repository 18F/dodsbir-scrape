import json

from dodsbirscrape import DODSBIRScrape

#initialize
i = DODSBIRScrape()

#get list of topic numbers from dodsbir.gov
i.get_topic_list()

#grab one topic
topic = i.get_topic("MDA14-004")

#get all topics and store them in a list (takes one second per topic)
i.get_all_topics(max=3)
i.save_as_json()
