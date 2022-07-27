from __future__ import annotations

from .interfaces import BusInterfaceAsync
from .exceptions import DatabaseWatcherException
from .databases import RedisBusPubSubAsync, RedisBusSimpleQueueAsync

async def connect_database_async(connection_string: str) -> BusInterfaceAsync:

    if connection_string.startswith("redis://"):
        return await RedisBusSimpleQueueAsync.open(connection_string)

    elif connection_string.startswith("redis+pubsub://"):
        return await RedisBusPubSubAsync.open(connection_string)

    else:
        raise DatabaseWatcherException(
            "Invalid database connection string URI"
        )

__all__ = ("connect_database_async",)
