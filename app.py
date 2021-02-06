import time

from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

REDIS_RETRY = 5

class Ticket():
    def __init__(self):
        cache.set('rear', 0)
        cache.set('current', 0)
        self.rear = cache.get('rear').decode('utf-8')
        self.current = cache.get('current').decode('utf-8')
    
    def get_current(self):
        self.current = self._get_key('current')
        return self.current

    def get_rear(self):
        self.rear = self._get_key('rear')
        return self.rear

    def incr_current(self):
        self.current = self._incr_key('current')
        return self.current
    
    def incr_rear(self):
        self.rear = self._incr_key('rear')
        return self.rear

    def _get_key(self, key):
        retries = REDIS_RETRY
        while True:
            try:
                val = cache.get(key)
                if not val:
                    return '0'
                return val.decode('utf-8')
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

    def _incr_key(self, key):
        retries = REDIS_RETRY
        while True:
            try:
                return cache.incr(key)
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)

ticket = Ticket()

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/retrieve_ticket')
def retrieve_ticket():
    return core('retrieve')

@app.route('/resolve_ticket')
def resolve_ticket():
    return core('resolve')

def core(action):
    rear = ticket.get_rear()
    current = ticket.get_current()
    if int(rear) < int(current):
        return  str(current)

    if action == 'retrieve':
        result = ticket.incr_rear()
    if action == 'resolve':
        if current < rear:
            result = ticket.incr_current()
        else:
            result = current
    return str(result)
