#!/usr/bin/env python3
""" 5. Implementing an expiring web cache and tracker """

import redis
import requests

def cache(expiration_time: int):
    def decorator(func):
        def wrapper(url):
            key = f"count:{url}"
            cache = redis.Redis()
            content = cache.get(url)
            if content is None:
                r = requests.get(url)
                content = r.content.decode()
                cache.setex(url, expiration_time, content)
            cache.incr(key)
            return content
        return wrapper
    return decorator

@cache(10)
def get_page(url: str) -> str:
    """
    Returns the HTML content of a particular URL.

    Args:
        url (str): The URL to retrieve.

    Returns:
        str: The HTML content of the URL.
    """
    r = requests.get(url)
    content = r.content.decode()
    key = f"count:{url}"
    cache = redis.Redis()
    cache.incr(key)
    cache.expire(key, 10)
    return content
