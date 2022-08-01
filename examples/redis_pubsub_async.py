import asyncio

from databases_watcher import connect_database_async

CONNECTION_STRING = "redis+pubsub://localhost:6501/?db=0&channel=default"

async def background_read_pubsub():
    redis_watch = await connect_database_async(CONNECTION_STRING)

    async for message in redis_watch.read_messages():
        print(message)
        break

    async for message in redis_watch.read_json_messages():
        print(message)
        break

async def main():
    redis_watch = await connect_database_async(CONNECTION_STRING)

    asyncio.create_task(background_read_pubsub())
    await asyncio.sleep(2)

    await redis_watch.send_message("hello!")
    await redis_watch.send_json_message({"message": "hello!"})

if __name__ == '__main__':
    asyncio.run(main())
