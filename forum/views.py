from pyramid.view import view_config
from forum.forumdata import TopicData
from forum.forumdata import MessageData
import datetime

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
	url = request.path_info
	return {'page_title': 'Forum', 'url': url}

@view_config(renderer='json', xhr=True, name='topic')
def my_view(request):
	topic_data = TopicData(request)
	message_data = MessageData(request)

	if 'list' in request.params:
		topics = topic_data.get_all_topics(50, 1)

		entries = []

		for topic in topics:
			entry = {'title': topic[u'title']}    
			entries.append(entry)

		return {'entries': entries}

	elif 'post' in request.params:
		
		if request.params['action_type'] == 'add':
			title = request.params['title']
			author = 'Thiago Pinho'
			message = request.params['topicText']
			date = datetime.datetime.utcnow()
			if topic_data.insert_topic(title, author, date):
				message_data.insert_message(title, message, date)
				return {'success': True, 'message': 'Topic saved'}
			return {'success': False, 'message': 'An error occurred'}

@view_config(renderer='json', xhr=True, name='messages')
def get_messages(request):
	message_data = MessageData(request)
	messages = message_data.get_all_messages(request.params['title'])
	entries  = []

	for message in messages:
		entry = {'_id': str(message[u'_id']), 'message': message[u'message'], 'date': message[u'date'].strftime("%B %d %Y")}
		entries.append(entry)

	return {'entries': entries}

@view_config(renderer='json', xhr=True, name="add_message")
def add_message(request):
	message_data = MessageData(request)
	message_data.insert_message(request.params['title'], request.params['message'], datetime.datetime.utcnow())

	return {'success': True, 'message': 'Message saved'}

@view_config(name='delete', xhr=True, request_method='DELETE', renderer='json')
def delete_topic(request):
	topic_data = TopicData(request)
	message_data = MessageData(request)
	title = request.params['title']
	message_data.delete_messages(title)
	topic_data.delete_topic(title)
	return {'success': True, 'message': 'Delete'}

@view_config(context='pyramid.httpexceptions.HTTPNotFound', renderer='templates/404_error.pt')
def not_found(request):
    return{'message': 'Page Not Found',  'cur_page': '', 'page_title': 'Requested Page Not Found'}
