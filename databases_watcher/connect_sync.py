from __future__ import annotations

from .interfaces import BusInterface
from .exceptions import DatabaseWatcherException
from .databases import RedisBusSimpleQueue, RedisBusPubSub

def connect_database(connection_string: str) -> BusInterface:

    if connection_string.startswith("redis://"):
        return RedisBusSimpleQueue.open(connection_string)

    elif connection_string.startswith("redis+pubsub://"):
        return RedisBusPubSub.open(connection_string)

    else:
        raise DatabaseWatcherException(
            "Invalid database connection string URI"
        )

__all__ = ("connect_database",)
