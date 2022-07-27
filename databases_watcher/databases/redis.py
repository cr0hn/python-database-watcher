from __future__ import annotations

from typing import Iterator

import redis
import orjson

from ..json_utils import read_json
from ..interfaces import BusInterface
from .redis_config import RedisConfig


class RedisBusSimpleQueue(BusInterface):

    def __init__(self, connection, queue: str, config: RedisConfig):
        self.queue = queue
        self.config = config
        self.connection: redis.Redis = connection

    def read_messages(self) -> Iterator[str|bytes|int|float]:

        while True:
            try:
                queue_name, message = self.connection.blpop(self.queue)
            except KeyboardInterrupt:
                return

            except:
                continue

            if message == "QUIT":
                break

            yield message

    def read_json_messages(self) -> Iterator[dict]:
        for message in self.read_messages():
            yield read_json(message)

    def send_message(self, data: dict or str or bytes or int or float):
        self.connection.rpush(self.queue, data)

    def send_json_message(self, data: dict):
        self.send_message(orjson.dumps(data))

    @classmethod
    def open(cls, connection_string: str) -> RedisBusSimpleQueue:
        config = RedisConfig.from_uri(connection_string)

        o = cls(
            connection=redis.Redis(
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


class RedisBusPubSub(BusInterface):

    def __init__(self, connection, channel: str, config: RedisConfig):
        self.config = config
        self.channel = channel
        self.connection: redis.Redis = connection

        self.pubsub = self.connection.pubsub()

    def read_messages(self) -> Iterator[str|bytes|int|float]:

        if "*" in self.channel:
            self.pubsub.psubscribe(self.channel)
        else:
            self.pubsub.subscribe(self.channel)

        while True:

            try:
                raw_message = self.pubsub.get_message()

                if raw_message.get("type") not in ("pmessage", "message"):
                    continue

                message = raw_message.get("data")
            except KeyboardInterrupt:
                return

            except:
                continue

            if message == "QUIT":
                break

            yield message

    def read_json_messages(self) -> Iterator[dict]:
        for message in self.read_messages():
            yield read_json(message)

    def send_message(self, data: dict or str or bytes or int or float):
        self.connection.publish(self.channel, data)

    def send_json_message(self, data: dict):
        self.send_message(orjson.dumps(data))

    @classmethod
    def open(cls, connection_string: str) -> RedisBusPubSub:
        config = RedisConfig.from_uri(connection_string)

        o = cls(
            connection=redis.Redis(
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

__all__ = ("RedisBusSimpleQueue", "RedisBusPubSub")
