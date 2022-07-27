from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlparse, parse_qsl

@dataclass
class RedisConfig:
    db: int = 0
    port: int = 6379
    user: str = None
    password: str = None
    host: str = "localhost"
    query_params: dict = field(default_factory=dict)

    @classmethod
    def from_uri(cls, uri: str) -> RedisConfig:
        parsed = urlparse(uri)
        query = dict(parse_qsl(parsed.query))

        return cls(
            db=int(query.pop("db", 0)),
            port=parsed.port,
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            query_params=query,
        )
