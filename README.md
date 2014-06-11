Python module for extracting DoD Small Business Innovation Research (SBIR) topics from http://dodsbir.net

## Examples

#### Get list of topic numbers
```python
from dodsbirscrape import DODSBIRScrape

#initialize
i = DODSBIRScrape()

#get list of topic numbers from dodsbir.gov
i.get_topic_list()

#see what you grabbed
print i.topic_ids

```

#### Get topic from topic number
```python
from dodsbirscrape import DODSBIRScrape

#initialize
i = DODSBIRScrape()

#get a topic based on id
topic = i.get_topic("SB142-004")

#see what you grabbed
print topic
```
