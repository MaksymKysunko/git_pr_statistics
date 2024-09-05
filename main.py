import redis

# Connect to Redis server
r = redis.Redis(host='localhost', port=6379, db=0)

# Set a value in Redis
r.set('hello', 'world')

# Retrieve the value from Redis
value = r.get('hello')

print(f'The value of "hello" is: {value.decode("utf-8")}')
