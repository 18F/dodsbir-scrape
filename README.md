Python module for extracting DoD Small Business Innovation Research (SBIR) topics from http://dodsbir.net

## Examples

#### Get list of topic numbers
```
from dodsbirscrape import DODSBIRScrape

#initialize
i = DODSBIRScrape()

#get list of topic numbers from dodsbir.gov
i.get_topic_list()

#see what you grabbed
print i.topic_ids

```
