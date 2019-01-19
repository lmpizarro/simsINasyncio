import redis
import time
import proceso

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

redis_instance = redis.Redis(connection_pool=pool)

proc = proceso.Proceso()

while True:
   counter = redis_instance.get('COUNTER')
   for tag in proc.get_tags():
       x = redis_instance.get(tag)
       print(counter, tag, x)
   time.sleep(1)
