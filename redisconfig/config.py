from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, urlunparse

from redis import Redis


@dataclass
class RedisConfig:
    host: str = "127.0.01"
    port: int = 6379
    db: int = 0
    ssl: bool = False
    password: str = None

    def connection(
        self, db: Optional[int] = None, password: Optional[str] = None, **kwargs
    ) -> Redis:
        params = kwargs.copy()
        params["host"] = self.host
        params["port"] = self.port
        params["db"] = db or self.db
        params["ssl"] = self.ssl
        params["password"] = password or self.password

        conn = Redis(**params)
        return conn

    @property
    def url(self) -> str:
        return to_url(self)


def from_url(url: str) -> RedisConfig:
    parts = urlparse(url)
    params = {
        "host": parts.hostname,
        "port": parts.port,
        "db": int(parts.path[1:].split("?", 1)[0] or 0),
        "ssl": parts.scheme == "rediss",
        "password": parts.password,
    }
    config = RedisConfig(**params)
    return config


def to_url(config: RedisConfig) -> str:
    scheme = "rediss" if config.ssl else "redis"
    netloc = f"{config.host}:{config.port}"
    if config.password:
        netloc = f":{config.password}@{netloc}"
    # parts tuple consists of the following:
    # scheme, netloc, path, params, query, fragment
    return urlunparse((scheme, netloc, str(config.db), None, None, None))


def config(url: Optional[str] = None) -> RedisConfig:
    """This method should use the url param or get the REDIS_URL
    from the environment, maybe have the pulling of that URL be it's own method
    so it could be easily tested, and return config from from_url()
    """
    pass


def connection(url: Optional[str] = None) -> Redis:
    """This method should create a config, optionally with the url param,
    call connection on that config and return it.
    """
    pass
