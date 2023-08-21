# Создать декоратор для использования кэша.
# Т.е. сохранять аргументы и результаты в словарь,
# если вызывается функция с агрументами,
# которые уже записаны в кэше - вернуть результат из кэша,
# если нет - выполнить функцию. Кэш лучше хранить в json.

import json
import hashlib
import os


def cache_decorator(cache_file):
    def decorator(func):
        def wrapper(*args, **kwargs):
            """Generate a unique hash based on function name, arguments,
            and keyword arguments."""
            hash_key = hashlib.sha1(json.dumps((func.__name__, args, kwargs),
                                               sort_keys=True).encode()).hexdigest()

            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                if hash_key in cache_data:
                    print("Попало в кэш!")
                    return cache_data[hash_key]

            result = func(*args, **kwargs)

            if os.path.exists(cache_file):
                with open(cache_file, 'r') as f:
                    cache_data = json.load(f)
                cache_data[hash_key] = result
            else:
                cache_data = {hash_key: result}

            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=4)

            return result
        return wrapper
    return decorator


CACHE_FILE = 'cache.json'


@cache_decorator(CACHE_FILE)
def expensive_function(n):
    print("Вычисляю")
    return n * 2


print(expensive_function(5))
print(expensive_function(5))
print(expensive_function(10))
