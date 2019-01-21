import asyncio
import time

counter1 = 0
counter2 = 0

async def firstWorker():
    global counter1
    while True:
        await asyncio.sleep(1)
        print("First Worker Executed")
        print('counter1', counter1)
        if counter1 > 2:
            break
        
async def secondWorker():
    global counter2
    while True:
        await asyncio.sleep(1)
        print("Second Worker Executed")
        print('counter2', counter2)
        if counter2 > 5:
            break

async def controller():
    global counter1
    global counter2
    while True:
        await asyncio.sleep(1)
        counter1 +=1
        counter2 +=1
        print("Controller", counter1, counter2)
        

tasks =[firstWorker(), secondWorker(), controller()]

loop = asyncio.get_event_loop()
try:
    [asyncio.ensure_future(t) for t in tasks]
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing Loop")
    loop.close()
