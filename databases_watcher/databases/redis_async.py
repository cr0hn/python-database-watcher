from __future__ import annotations

from typing import Iterator, AsyncIterable

import orjson
import aioredis

from ..json_utils import read_json
from .redis_config import RedisConfig
from ..interfaces import BusInterfaceAsync


class RedisBusSimpleQueueAsync(BusInterfaceAsync):

    def __init__(self, connection, queue: str, config: RedisConfig):
        self.queue = queue
        self.config = config
        self.connection: aioredis.Redis = connection

    async def read_messages(self) -> AsyncIterable[str | bytes | int | float]:

        while True:
            try:
                queue_name, message = await self.connection.blpop(self.queue)
            except KeyboardInterrupt:
                return

            except:
                continue

            if message == "QUIT":
                break

            yield message

    async def read_json_messages(self) -> Iterator[dict]:
        async for message in self.read_messages():
            yield read_json(message)

    async def send_message(self, data: memoryview or str or bytes or int or float):
        await self.connection.rpush(self.queue, data)

    async def send_json_message(self, data: dict):
        await self.send_message(orjson.dumps(data))

    @classmethod
    async def open(cls, connection_string: str) -> RedisBusSimpleQueueAsync:
        config = RedisConfig.from_uri(connection_string)

        o = cls(
            connection=aioredis.Redis(
                host=config.host,
                port=config.port,
                db=config.db,
                password=config.password,
                username=config.user,
            ),
            queue=config.query_params.get("queue", "default"),
            config=config,
        )

        return o


class RedisBusPubSubAsync(BusInterfaceAsync):

    def __init__(self, connection, channel: str, config: RedisConfig):
        self.config = config
        self.channel = channel
        self.connection: aioredis.Redis = connection

        self.pubsub = self.connection.pubsub()

    async def read_messages(self) -> AsyncIterable[str | bytes | int | float]:

        if "*" in self.channel:
            await self.pubsub.psubscribe(self.channel)
        else:
            await self.pubsub.subscribe(self.channel)

        while True:

            try:
                raw_message = await self.pubsub.get_message(
                    ignore_subscribe_messages=True
                )

                message = raw_message.get("data")
            except KeyboardInterrupt:
                return

            except:
                continue

            if message == "QUIT":
                break

            yield message

    async def read_json_messages(self) -> Iterator[dict]:
        async for message in self.read_messages():
            yield read_json(message)

    async def send_message(self, data: dict or str or bytes or int or float):
        await self.connection.publish(self.channel, data)

    async def send_json_message(self, data: dict):
        await self.send_message(orjson.dumps(data))

    @classmethod
    async def open(cls, connection_string: str) -> RedisBusPubSubAsync:
        config = RedisConfig.from_uri(connection_string)

        o = cls(
            connection=aioredis.Redis(
                host=config.host,
                port=config.port,
                db=config.db,
                password=config.password,
                username=config.user,
            ),
            channel=config.query_params.get("channel", "default"),
            config=config,
        )

        return o


__all__ = ("RedisBusSimpleQueueAsync", "RedisBusPubSubAsync")
