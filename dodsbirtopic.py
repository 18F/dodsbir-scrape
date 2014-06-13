import json

class DODSBIRTopic:
	"""base class for DOD SBIR Topics"""
	def __init__(self):
		pass

	def as_json(self):
		return json.dumps(self.__dict__)

	def __str__(self):
		if self.title:
			return "%s" % self.title
		else:
			return self
