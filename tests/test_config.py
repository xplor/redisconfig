import os
from unittest import mock
from urllib.parse import urlparse

import pytest

import redisconfig
from redisconfig.config import DEFAULT_ENV_VAR, DEFAULT_HOST, DEFAULT_PORT


def test_config_defaults():
    config = redisconfig.RedisConfig()
    assert not config.ssl
    assert config.host == DEFAULT_HOST
    assert config.port == DEFAULT_PORT
    assert config.password is None
    assert config.db == 0


def test_from_url():
    url = "redis://:badpassword@example.com:1234/3"
    config = redisconfig.from_url(url)
    assert not config.ssl
    assert config.host == "example.com"
    assert config.port == 1234
    assert config.password == "badpassword"
    assert config.db == 3


def test_from_url_ssl():
    url = "rediss://"
    config = redisconfig.from_url(url)
    assert config.ssl


def test_from_url_ignore_params():
    url = "rediss:///3?ignoreme=true"
    config = redisconfig.from_url(url)
    assert config.db == 3


def test_to_url():
    config = redisconfig.RedisConfig(host="example.com", port=1234, db=3)
    url = redisconfig.to_url(config)
    assert url == "redis://example.com:1234/3"


def test_to_url_ssl():
    config = redisconfig.RedisConfig(ssl=True)
    url = redisconfig.to_url(config)
    assert url == "rediss://127.0.0.1:6379/0"


def test_config_to_url():
    config = redisconfig.RedisConfig(
        host="example.com", port=1234, db=5, password="badpassword", ssl=True
    )
    url = config.url
    assert url == "rediss://redis:badpassword@example.com:1234/5"


def test_url_config():
    config = redisconfig.config("rediss://:badpassword@example.com:1234/5")
    assert config.ssl
    assert config.host == "example.com"
    assert config.port == 1234
    assert config.password == "badpassword"
    assert config.db == 5


@mock.patch.dict(
    os.environ, {DEFAULT_ENV_VAR: "rediss://:badpassword@example.com:1234/5"}
)
def test_env_config():
    config = redisconfig.config()
    assert config.ssl
    assert config.host == "example.com"
    assert config.port == 1234
    assert config.password == "badpassword"
    assert config.db == 5


def test_config_no_url_error():
    with pytest.raises(ValueError):
        config = redisconfig.config()


@mock.patch.dict(os.environ, {DEFAULT_ENV_VAR: "rediss:///5"})
def test_url_from_env_default():
    url = redisconfig.url_from_env()
    assert url == "rediss:///5"


@mock.patch.dict(os.environ, {"REDIS_WORKER_URL": "rediss:///10"})
def test_url_from_env_custom():
    url = redisconfig.url_from_env("REDIS_WORKER_URL")
    assert url == "rediss:///10"
