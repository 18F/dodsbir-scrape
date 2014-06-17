from datetime import datetime
from time import mktime
import json

class TopicEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)


class DODSBIRTopic:
	"""base class for DOD SBIR Topics"""
	def __init__(self):
		pass

	def __json__(self):
		return json.dumps(self.__dict__, cls=TopicEncoder)

	def __str__(self):
		if self.title:
			return "%s" % self.title
		else:
			return self
