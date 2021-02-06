from flask import Flask
app = Flask(__name__)

class Ticket():
    def __init__(self):
        self.rear = 0
        self.current = 0
    
    def get_current(self):
        return self.current

    def get_rear(self):
        return self.rear

    def incr_current(self):
        self.current += 1
        return self.current
    
    def incr_rear(self):
        self.rear += 1
        return self.rear

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
    if rear < current:
        return  str(current)
    if action == 'retrieve':
        result = ticket.incr_rear()
    if action == 'resolve':
        if current < rear:
            result = ticket.incr_current()
        else:
            result = current
    return str(result)
