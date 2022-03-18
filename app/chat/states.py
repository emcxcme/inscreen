from hashlib import md5

_MEMCACHE = dict()


def _generate_id_from(arg: str) -> int:
    if arg in _MEMCACHE.keys():
        return _MEMCACHE[arg]
    encoded_arg = arg.encode("utf-8")
    hashed_arg = md5(encoded_arg)
    hexdigest = hashed_arg.hexdigest()
    id = int(hexdigest, 16)
    _MEMCACHE[arg] = id
    return id


SELECTING_ORGANIZATION = _generate_id_from("SELECTING_ORGANIZATION")
