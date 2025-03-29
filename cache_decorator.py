import hashlib
import functools
import json

def cache_memory(maxsize=100):
    def decorator(func):
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def make_hashable(obj):
                if isinstance(obj, list):
                    return tuple(make_hashable(item) for item in obj)
                if isinstance(obj, dict):
                    return tuple(sorted((k, make_hashable(v)) for k, v in obj.items()))
                return obj  # Tipos imutáveis são retornados como estão

            hashable_args = tuple(make_hashable(arg) for arg in args)
            hashable_kwargs = tuple((k, make_hashable(v)) for k, v in kwargs.items())

            # Criar chave de cache única
            key_str = json.dumps((hashable_args, hashable_kwargs), sort_keys=True)
            cache_key = hashlib.md5(key_str.encode()).hexdigest()

            # Verificar se o valor já está no cache
            if cache_key in cache:
                return cache[cache_key]

            # Se não estiver no cache, executa a função e armazena o resultado
            result = func(*args, **kwargs)

            # Manter o cache limitado ao `maxsize`
            if len(cache) >= maxsize:
                cache.pop(next(iter(cache)))  # Remove o item mais antigo

            cache[cache_key] = result
            return result

        return wrapper
    return decorator
