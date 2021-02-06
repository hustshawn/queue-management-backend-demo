import time

from flask import Flask
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


class Ticket():
    def __init__(self):
        cache.set('rear', 0)
        cache.set('current', 0)
        self.rear = cache.get('rear').decode('utf-8')
        self.current = cache.get('current').decode('utf-8')
    
    def get_current(self):
        current = cache.get('current')
        if not current:
            return '0'
        self.current = current.decode('utf-8')
        return self.current

    def get_rear(self):
        self.rear = cache.get('rear').decode('utf-8')
        return self.rear

    def incr_current(self):
        self.current = cache.incr('current')
        return self.current
    
    def incr_rear(self):
        self.rear = cache.incr('rear')
        return self.rear


ticket = Ticket()

def incr_key(key):
    retries = 5
    while True:
        try:
            return cache.incr(key)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

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
