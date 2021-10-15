from urllib.parse import urlparse

import redisconfig


def test_config_defaults():
    config = redisconfig.RedisConfig()
    assert not config.ssl
    assert config.host == "127.0.01"
    assert config.port == 6379
    assert config.password is None
    assert config.db == 0


def test_from_url():
    url = "redis://:notagoodpassword@example.com:1234/3"
    config = redisconfig.from_url(url)
    assert not config.ssl
    assert config.host == "example.com"
    assert config.port == 1234
    assert config.password == "notagoodpassword"
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
    assert url == "rediss://127.0.01:6379/0"


def test_config_to_url():
    config = redisconfig.RedisConfig(
        host="example.com", port=1234, db=5, password="badpassword", ssl=True
    )
    url = config.url
    assert url == "rediss://:badpassword@example.com:1234/5"
