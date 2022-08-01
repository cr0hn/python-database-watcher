import asyncio

from databases_watcher import connect_database_async

async def main():
    redis_watch = await connect_database_async("redis://localhost:6501/?db=0&queue=default")

    await redis_watch.send_message("hello!")
    await redis_watch.send_json_message({"message": "hello!"})

    async for message in redis_watch.read_messages():
        print(message)
        break

    async for message in redis_watch.read_json_messages():
        print(message)
        break


if __name__ == '__main__':

    asyncio.run(main())
