import asyncio
import time

async def myTask():
    await asyncio.sleep(1)
    print("Processing Task")

async def myTaskGenerator():
    for i in range(5):
        asyncio.ensure_future(myTask())

start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(myTaskGenerator())
print("Completed All Tasks")
loop.close()

end = time.time()  
print("Total time: {}".format(end - start))
