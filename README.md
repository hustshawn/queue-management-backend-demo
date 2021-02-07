Restaurant Queue Management Backend Demo
===

Inspired by the Gulu App, tried to implement a simple demo for the restaurant queue management backend with Flask and Redis.


## Run
```
docker-compose up
```

## APIs

With `GET` method, access below APIs from browser via `http://127.0.0.1:5000`
- `/retrieve_ticket`, simulate the customer retrive a ticket remotely and waiting at the rear of the queue.
- `/resolve_ticket`,  simulate the restaurant that provide a seat to the customer outside.
