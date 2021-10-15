from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, urlunparse

import redis


@dataclass
class RedisConfig:
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    ssl: bool = False
    password: str = None

    def connection(self, db: Optional(int) = None, password: Optional(str) = None, **kwargs):
        params = kwargs.copy()
        params["host"] = self.host
        params["port"] = self.port
        params["db"] = db or self.db
        params["ssl"] = self.ssl
        params["password"] = password or self.password

        conn = redis.Redis(**params)
        return conn

    @property
    def url(self) -> str:
        return to_url(self)


def from_url(url: str) -> RedisConfig:
    parts = urlparse(url)
    params = {
        "host": parts.hostname,
        "port": parts.port,
        "db": int(parts.path.strip("/") or 0),
        "ssl": parts.scheme == "rediss",
        "password": parts.password,
    }
    config = RedisConfig(**params)
    return config


def to_url(config: RedisConfig) -> str:
    scheme = "rediss" if config.ssl else "redis"
    netloc = "{config.host}:{config.port}"
    if config.password:
        netloc = ":{config.password}@{netloc}"
    # parts tuple consists of the following:
    # scheme, netloc, path, params, query, fragment
    return urlunparse((scheme, netloc, config.db, None, None, None))