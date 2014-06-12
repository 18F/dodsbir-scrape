Python module for extracting DoD Small Business Innovation Research (SBIR) topics from http://dodsbir.net

## Examples

#### Get list of topic numbers
```python
from dodsbirscrape import DODSBIRScrape

#initialize
s = DODSBIRScrape()

#get list of topic numbers from dodsbir.gov
s.get_topic_list()

#see what you grabbed
print s.topic_ids

```

#### Get topic from topic number
```python
from dodsbirscrape import DODSBIRScrape

#initialize
s = DODSBIRScrape()

#get a topic based on topic number
topic = s.get_topic("SB142-004")

#see what you grabbed
print topic

```

## Bugs and Limitations

- The scraper doesn't retrieve questions and answers associated with topics.
- The 'Proposals Accepted' date range isn't currently parsed and should be.
