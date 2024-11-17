# cache_handler.py
# Ron Company #


import time

class CacheManager:
    def __init__(self):
        self.cache = {}
        self.cache_times = {}

    def set_cache(self, key, value):
        self.cache[key] = value
        self.cache_times[key] = time.time()

    def get_cache(self, key, cache_duration):
        if key in self.cache and (time.time() - self.cache_times[key]) < cache_duration:
            return self.cache[key]
        return None

cache_manager = CacheManager()
