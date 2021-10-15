# redisconfig

Simple, robust Redis configuration for Python

## Installation

```
pipenv install redisconfig
```

## Basic Usage

```
>>> import redisconfig

>>> config = redisconfig.RedisConfig()
RedisConfig(host='127.0.0.1', port=6379, db=0, ssl=False, password=None)

>>> config.host
'127.0.0.1'

>>> config.url()
'redis://127.0.0.1:6379/0'

>>> config.connection()
Redis<ConnectionPool<Connection<host=127.0.0.1,port=6379,db=0>>>
```

### REDIS_URL Environment Variable

In many cases the Redis connection URL is stored in the REDIS_URL environment variable. redisconfig will use that value as a default for several operations, such as the module-level config() and connection() methods. With an environment variable of `REDIS_URL=rediss://noop:badpassword@10.0.0.1/2`:

```
>>> redisconfig.config()
RedisConfig(host='10.0.0.1', port=6379, db=2, ssl=True, password='badpassword')

>>> redisconfig.connection()
Redis<ConnectionPool<SSLConnection<host=10.0.0.1,port=6379,db=2>>>
```

### Update Configuration Values

You can update values directly like `config.db = 5` but sometimes you want to change values without changing the underlying configuration. The url() and replace() methods on RedisConfig allow you to make new urls or configs without changing the original values.

Create a new URL:

```
>>> config = redisconfig.RedisConfig()
>>> config.url()
'redis://127.0.0.1:6379/0'

>>> config.url(db=2)
'redis://127.0.0.1:6379/2'
```

Create a new RedisConfig instance:

```
>>> config.replace(db='10.0.0.1')
RedisConfig(host='10.0.0.1', port=6379, db=0, ssl=False, password=None)
```

## Developing

```
pipenv install --dev
```

## Testing

```
pipenv run pytest
```
