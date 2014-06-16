import json

from dodsbirscrape import DODSBIRScrape

#initialize
i = DODSBIRScrape()

#stage solicitation
i.stage_current_solicitation()

#grab one topic
topic = i.get_topic("MDA14-004")
print topic.__json__()

#get all topics and store them in a list (takes one second per topic)
i.get_all_topics(max=3)
i.save_as_json()
