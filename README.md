# Python Database Watcher Library

![License](https://img.shields.io/badge/License-Apache2-SUCCESS)
![Pypi](https://img.shields.io/pypi/v/databases_watcher)
![Python Versions](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue)

In a nutshell ``Python Database Watcher Library`` is a small library with a set of utilities to help you to monitor and watch the database changes.

# Install

```bash
> pip install databases_watcher
```

# Supported databases

## Redis

Supported modes:

- **Queue watch mode**: `redis://[[user]:[password]]@host:port/?db=[INT]&queue=[STRING]`
- **Pub/Sub mode**: `redis+pubsub://[[user]:[password]]@host:port/?db=[INT]&channel=[STRING]`
- **Changes watch mode** (TODO): `redis+watch://[[user]:[password]]@host:port/?db=[INT]&queue=[STRING]`

> TODO: improve watch mode

# Usage examples

## Redis

### Queue watch mode (Sync mode)

```python
from databases_watcher import connect_database

def main():
    redis_watch = connect_database("redis://localhost:6501/?db=0&queue=default")

    redis_watch.send_message("hello!")
    redis_watch.send_json_message({"message": "hello!"})

    print(next(redis_watch.read_messages()))
    print(next(redis_watch.read_json_messages()))


if __name__ == '__main__':
    main()
```

### Queue watch mode (Async mode)

```python
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

```

### Pub/Sub watch mode (Sync mode)

```python
import time
import threading

from databases_watcher import connect_database

CONNECTION_STRING = "redis+pubsub://localhost:6501/?db=0&channel=default"

def background_read_pubsub():
    redis_watch = connect_database(CONNECTION_STRING)

    print(next(redis_watch.read_messages()))
    print(next(redis_watch.read_json_messages()))


def main():
    redis_watch = connect_database(CONNECTION_STRING)

    t = threading.Thread(target=background_read_pubsub)
    t.start()

    time.sleep(2)

    redis_watch.send_message("hello!")
    redis_watch.send_json_message({"message": "hello!"})

    t.join()

if __name__ == '__main__':
    main()

```

### Pub/Sub watch mode (Async mode)

```python
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

```

# License

Dictionary Search is Open Source and available under the [MIT](https://github.com/cr0hn/python-performance-tools/blob/main/LICENSE).

# Contributions

Contributions are very welcome. See [CONTRIBUTING.md](https://github.com/cr0hn/python-performance-tools/blob/main/CONTRIBUTING.md) or skim existing tickets to see where you could help out.


