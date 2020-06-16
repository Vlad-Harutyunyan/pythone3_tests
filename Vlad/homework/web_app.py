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

    if len(data) != len(expected_keys):
        raise HTTPError('Bad Request', 400)

    for key in expected_keys:
        if key not in data:
            raise HTTPError('Bad Request', 400)

    store_in_db(data)
    return get_feedback(env)

def search_in_db(search:dict)  -> list :
    initfile = os.path.join(thisfolder, 'db.json')

    with open(initfile,'r') as json_db:
        db_data = json.load(json_db)
    if not search :
        return 
    find_elemets = []
    for item in db_data:
        for key in item :
            if item[key][0] == search['user_search'][0]:
                find_elemets.append(item)
        
    return find_elemets

def get_search(env: dict):
    payload = env['QUERY_STRING']
    data = parse_qs(payload)
    data_from_db = search_in_db(data) 
    if data_from_db:
        print('find something')
        return [f'<h2>find something</h2>'.encode()]
          
    with open(Path(f'{thisfolder}/html/search.html'), 'rb') as fd:
        return fd.read()
    

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
    '/search': {
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
