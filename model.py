import aioredis
import asyncio
import time
import proceso
import aiohttp
from aiohttp import web


async def main():
    pool = await aioredis.create_redis_pool('redis://localhost')
    sr = 1
    counter = 0

    proc = proceso.Proceso()


    while True:
       t_init = time.time()
       counter += 1
       await pool.set('COUNTER', counter)
       
       proc.set_time(counter)
       for tag in proc.get_states():
           await pool.set(tag, proc.get_states()[tag])


       print(counter, proc)
       t_end = time.time()
       await asyncio.sleep(sr - (t_end - t_init))


async def get_state_model():
    pool = await aioredis.create_redis_pool('redis://localhost')
    # pool = await aioredis.create_connection('redis://localhost')

    proc = proceso.Proceso()

    while True:
       counter = await pool.get('COUNTER')
       for tag in proc.get_tags():
           x = await pool.get(tag)
           proc.tags[tag]['var'] = x
       print(counter, proc)
       await asyncio.sleep(1)


async def wshandler(request):
    pool = await aioredis.create_redis_pool('redis://localhost')

    proc = proceso.Proceso()

    ws = web.WebSocketResponse(autoclose=False)
    is_ws = ws.can_prepare(request)
    if not is_ws:
        return web.HTTPBadRequest()

    await ws.prepare(request)

    while True:
        msg = await ws.receive()
         
        print(msg)
        if msg.type == web.WSMsgType.text:


            # await ws.send_str(msg.data)

            if msg.data == 'close':
                await ws.close()
            elif msg.data == 'state':
                counter = await pool.get('COUNTER')
                for tag in proc.get_tags():
                    x = await pool.get(tag)
                    proc.tags[tag]['var'] = x
                print(counter)
                       
                await ws.send_str(str(proc))

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

        elif msg.type == web.WSMsgType.close:
            await ws.close()
            break
        else:
            break

    return ws

async def server(loop):
    app = web.Application()
    
    app.add_routes([web.get('/', handle), web.get('/state', wshandler)])

    handler = app._make_handler()
    srv = await loop.create_server(handler, '127.0.0.1', 9001)
    print("Server started at http://127.0.0.1:9001")
    return app, srv, handler

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def finish(app, srv, handler):
    srv.close()
    await handler.shutdown()
    await srv.wait_closed()


if __name__ == '__main__':
 
    loop = asyncio.get_event_loop()

    tasks = [  
        asyncio.ensure_future(main()),
        asyncio.ensure_future(get_state_model())
    ]

    app, srv, handler = loop.run_until_complete(server(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(finish(app, srv, handler))    
    loop.close()
