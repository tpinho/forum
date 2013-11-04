class TopicData(object):
	def __init__(self, request):
		self.settings = request.registry.settings
		self.collection = request.db['forumTopics']

	def get_all_topics(self, num_of_entries, page):
		row = num_of_entries * (page - 1)
		entries = self.collection.find({}, {'bodyText': 0}).sort('_id', -1)[row: row + num_of_entries]
		return entries

	def get_topic_by_title(self, title):
		topic = self.collection.find_one({'title': title})
		return topic

	def delete_topic(self, title):
		self.collection.remove({'title': title})
		return True

	def insert_topic(self, title, author, date):
		if self.get_topic_by_title(title) is None:
			topic_data = dict()
			topic_data['title'] = title
			topic_data['author'] = author
			topic_data['date'] = date
			self.collection.insert(topic_data, safe=True)
			return True
		return False

class MessageData(object):
	def __init__(self, request):
		self.settings = request.registry.settings
		self.collection = request.db['forumMessages']

	def get_all_messages(self, titleTopic):
		messages = self.collection.find({'titleTopic': titleTopic})
		return messages

	def delete_messages(self, titleTopic):
		self.collection.remove({'titleTopic': titleTopic})
		return True

	def insert_message(self, titleTopic, message, date):
		message_data = dict()
		message_data['titleTopic'] = titleTopic
		message_data['message'] = message
		message_data['date'] = date
		self.collection.insert(message_data, safe=True)