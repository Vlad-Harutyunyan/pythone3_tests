from pathlib import Path
from urllib.parse import parse_qs
from typing import Callable, Iterable
from wsgiref.simple_server import make_server
import os
import json 

#absolute path
thisfolder = os.path.dirname(os.path.abspath(__file__))
def content_type(path):                                                          
    if path.endswith(".css"):                                                    
        return "text/css"                                                        
    else:                                                                        
        return "text/html" 
        
class HTTPError(Exception):

    def __init__(self, reason: str, code: int):
        self.code = code
        self.reason = reason
        super().__init__(reason)


def get_feedback(env: dict):
    print(Path('html/feedback.html'))
    with open(Path(f'{thisfolder}/html/feedback.html'), 'rb') as fd:
        return fd.read()

#Storing inputed dict in json file 
def store_in_db(data:dict) -> None :

    initfile = os.path.join(thisfolder, 'db.json')
    old_data = []
    if not os.path.isfile(initfile):
        old_data.append(data)
        with open(initfile, mode='w') as f:
            f.write(json.dumps(old_data, indent=2))
    else:
        with open(initfile) as feedsjson:
            feeds = json.load(feedsjson)
        feeds.append(data)
        with open(initfile, mode='w') as f:
            f.write(json.dumps(feeds, indent=2))

 

def post_feedback(env: dict):
    expected_keys = ('user_email', 'feedback_message','user_name')
    payload = env['wsgi.input'].read(int( env['CONTENT_LENGTH'] ))

    data = parse_qs(payload.decode())
    store_in_db(data)

    if len(data) != len(expected_keys):
        raise HTTPError('Bad Request', 400)

    for key in expected_keys:
        if key not in data:
            raise HTTPError('Bad Request', 400)

    return get_feedback(env)


def get_search(env: dict):
    pass


def post_search(env: dict):
    pass


def not_found(env: dict):
    raise HTTPError('Not Found', 404)



ROUTING_TABLE = {
    '/feedback': {
        'GET': get_feedback,
        'POST': post_feedback,
    },
    '/feedback/send': {
        'POST': post_feedback,
    },
    '/login': {
        'GET': get_search,
        'POST': post_search,
    }
}


def app(env: dict, start_response: Callable) -> Iterable:
    # for key, val in env.items():
    #    print(key, '=', val)

    route = env['PATH_INFO']
    method = env['REQUEST_METHOD']

    try:
        handler = ROUTING_TABLE.get(route, {}).get(method, not_found)
        response = handler(env)
        headers = []                                                                 
        headers.append(("Content-Type", content_type(route)))  
        start_response('200 OK',headers)
        return [response]

    except HTTPError as herr:
        start_response(f'{herr.code} {herr.reason}', [('Content-type', 'text/html')])
        return [f'<h2>{herr.code} {herr.reason}</h2>'.encode()]


if __name__ == '__main__':
    port = 8003
    with make_server('', port, app) as httpd:
        print(f'Serving on port {port}...')
        httpd.serve_forever()
