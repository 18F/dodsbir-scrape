class DODSBIRTopic:
	"""base class for DOD SBIR Topics"""
	def __init__(self):
		pass

	def __str__(self):
		if self.title:
			return "%s" % self.title
		else:
			return self
