import requests


COMMON_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100'

def requests_get(*args, **kwargs):
    if 'headers' not in kwargs:
        kwargs['headers'] = {}
    kwargs['headers']['user-agent'] = COMMON_UA
    return requests.get(*args, **kwargs)
