from aiohttp import web
import aiohttp
import asyncio


async def main():
    session = aiohttp.ClientSession()

    try:
        ws = await session.ws_connect('ws://127.0.0.1:9001/state')
    except Exception as e:
        print(e)
        exit()

   
    while True:
        await asyncio.sleep(1)
        try:
            await ws.send_str('state')
        except Exception as e:
            print(e)
            exit()

        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    if msg.data == 'close cmd':
                        await ws.close()
                        break
                    else:
                        print(msg.data)
                        break
       
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
        except Exception as e:
            print(e)
            exit()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    tasks = [  
        asyncio.ensure_future(main())
    ]

    loop.run_until_complete(asyncio.wait(tasks))  
    loop.close()

