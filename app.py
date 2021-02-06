import time
from datetime import datetime, date, time, timedelta

from flask import Flask
import redis

REDIS_RETRY = 5
REDIS_HOST = 'redis'
REDIS_PORT = 6379

app = Flask(__name__)
cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

today_start = datetime.combine(date.today(), time()) 
next_day = today_start + timedelta(1)


class Ticket():
    def __init__(self):
        cache.set('rear', 0)
        cache.expireat('rear', next_day)
        self.rear = 0
        cache.set('current', 1)
        cache.expireat('current', next_day)
        self.current = 1
    
    def get_current(self):
        self.current = self._cache_op('get', 'current')
        return int(self.current)

    def get_rear(self):
        self.rear = self._cache_op('get', 'rear')
        return int(self.rear)

    def incr_current(self):
        self.current = self._cache_op('incr', 'current')
        return self.current
    
    def incr_rear(self):
        self.rear = self._cache_op('incr', 'rear')
        return self.rear

    def _cache_op(self, action, key):
        retries = REDIS_RETRY
        while True:
            try:
                if action == 'incr':
                    return cache.incr(key)
                elif action == 'get':
                    return cache.get(key)
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
    rear, current = core('retrieve')
    msg = {
        "your_number": rear,
        "current": current,
        "msg": "{} in front of you".format(str(rear-current))
    }
    return msg

@app.route('/resolve_ticket')
def resolve_ticket():
    rear, current = core('resolve')
    msg = {
        "rear_number": rear,
        "current": current,
        "msg": "{} customer is wating outside".format(str(rear-current))
    }
    return msg

def core(action):
    rear = ticket.get_rear()
    current = ticket.get_current()
    if rear < current and rear >= 1:
        return  current, current

    if action == 'retrieve':
        rear = ticket.incr_rear()
    if action == 'resolve':
        if current < rear:
            current = ticket.incr_current()
        else:
            rear = current
    return rear, current
