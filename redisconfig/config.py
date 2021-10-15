import os
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, urlunparse, parse_qs

from redis import Redis

DEFAULT_ENV_VAR = "REDIS_URL"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 6379


@dataclass
class RedisConfig:
    """
    Represents configuration for a Redis connection.
    """

    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    db: int = 0
    ssl: bool = False
    password: str = None

    def connection(
        self, db: Optional[int] = None, password: Optional[str] = None, **kwargs
    ) -> Redis:
        """
        Create a Redis connection from the current config values.

        Parameters
        ----------
        db : int, optional
            Overrides the config db value (default is None)
        password : str, optional
            Overrides the config password value (default is None)
        kwargs:
            Any valid parameter for redis.Redis()

        Returns
        -------
        redis.Redis
        """
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
        """Convert the current config values into a URL"""
        return to_url(self)


def url_from_env(var: Optional[str] = None) -> str:
    """
    Retrieve a Redis URL from an environment variable.
    If var is not specified the default of REDIS_URL will be used.
    None will be returned if no value exists for var.

    Parameters
    ----------
    var : str, optional
        Specify the environment variable to read from

    Returns
    -------
    str
    """
    value = os.environ.get(var or DEFAULT_ENV_VAR)
    return value


def from_url(url: str) -> RedisConfig:
    """
    Create a Redis configuration from a URL.

    Parameters
    ----------
    url : str
        Redis URL as string

    Returns
    -------
    RedisConfig
    """
    if url:
        parts = urlparse(url)
        qs_args = parse_qs(parts.query)

        if "db" in qs_args:
            db = int(qs_args["db"][0])
        elif parts.path:
            # strip off the beginning / and convert to int
            db = int(parts.path[1:])
        else:
            db = 0

        kwargs = {
            "host": parts.hostname,
            "port": parts.port,
            "db": db,
            "ssl": parts.scheme == "rediss",
            "password": parts.password,
        }
        config = RedisConfig(**kwargs)
        return config


def to_url(config: RedisConfig) -> str:
    """
    Converts a Redis configuration into a URL.

    If the connection has a password, a dummy username of redis will be
    added to the URL. Usernames are not used in Redis so this value
    can be safely ignored.

    Parameters
    ----------
    config : RedisConfig
        RedisConfig instance

    Returns
    -------
    str
    """
    scheme = "rediss" if config.ssl else "redis"
    netloc = f"{config.host}:{config.port}"
    if config.password:
        netloc = f"redis:{config.password}@{netloc}"
    # Parts tuple consists of the following:
    # scheme, netloc, path, params, query, fragment
    return urlunparse((scheme, netloc, str(config.db), None, None, None))


def config(url: Optional[str] = None) -> RedisConfig:
    """
    Create a Redis configuration from a URL.
    If no url is given the URL will attempt to be read
    from the REDIS_URL environment variable.
    A ValueError will be raised if no valid URL is found.

    Parameters
    ----------
    url : str, optional
        A Redis connection URL

    Returns
    -------
    RedisConfig
    """
    if not url:
        url = url_from_env()
    config = from_url(url)
    if not config:
        raise ValueError(f"Invalid Redis URL or missing environment variable")
    return config


def connection(url: Optional[str] = None) -> Redis:
    """
    Create a Redis connection a URL. If url is not specified
    the REDIS_URL environment variable will be used.
    A ValueError will be raised if no valid URL is found.

    Parameters
    ----------
    url : str, optional
        A Redis connection URL

    Returns
    -------
    redis.Redis
    """
    return config(url).connection()
