from dodsbirscrape import DODSBIRScrape

i = DODSBIRScrape()
i.get_topic_list()

topic = i.get_topic("MDA14-004")

print "Topic Number: %s\n" % topic.topic_number
print "Title: %s\n" % topic.title
print "Program: %s\n" % topic.program 
print "Areas: %s\n" % topic.areas
print "URL: %s\n" % topic.url
print "Program: %s\n" % topic.acquisition_program 
print "Objective: %s\n" % topic.objective
print "Description: %s\n" % topic.description
print "Phases: %s\n" % topic.phases
print "References: %s\n" % topic.references
print "Keywords: %s\n" % topic.keywords

i.get_all_topics()
