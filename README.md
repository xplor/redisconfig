# redisconfig
Simple, robust Redis configuration for Python


## Some thoughts

```
>>> import redisconfig
>>> rc = redisconfig.config()
# load from REDIS_URL env by default or use a url parameter passed to config
# would love to use a dataclasss here, just for the sake of using it :)
<RedisConfig: host=x, port=x, ...>

>>> rc.host
"cache.theredishost.com"

>>> rc.connection()
# actually create a redis connection from the config
# optional database= parameter

>>> redisconfig.connection()
# shortcut for redisconfig.config().connection
```

There's also this pattern of iterating the databases, but not sure the best way to do that yet.
