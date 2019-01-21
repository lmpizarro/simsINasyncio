import redis
import time
import proceso

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

redis_instance = redis.Redis(connection_pool=pool)

sr = 1
counter = 0

proc = proceso.Proceso()

if __name__ == '__main__':

    while True:
       t_init = time.time()
       counter += 1
       redis_instance.set('COUNTER', counter)
       
       proc.set_time(counter)
       for tag in proc.get_states():
           redis_instance.set(tag, proc.get_states()[tag])


       print(counter, proc)
       t_end = time.time()
       time.sleep(sr - (t_end - t_init))
