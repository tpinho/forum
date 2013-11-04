from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid_beaker import session_factory_from_settings
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
import pymongo
from forum.resources import Root


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    session_factory = session_factory_from_settings(settings)

    authn_policy = AuthTktAuthenticationPolicy('A@uth3ntic@t3')
    authz_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory=Root,  authentication_policy=authn_policy,  authorization_policy=authz_policy,  session_factory=session_factory)

    # MongoDB
    def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        event.request.db = db

    db_uri = settings['mongodb.url']
    MongoDB = pymongo.Connection
    if 'pyramid_debugtoolbar' in set(settings.values()):
        class MongoDB(pymongo.Connection):
            def __html__(self):
                return 'MongoDB: <b>{}></b>'.format(self)

    conn = MongoDB(db_uri)
    config.registry.settings['mongodb_conn'] = conn
    config.add_subscriber(add_mongo_db, NewRequest)

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'forum:static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan('forum')
    return config.make_wsgi_app()
