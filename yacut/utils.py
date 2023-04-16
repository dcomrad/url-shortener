from random import choice, randrange

from .models import URLMap

ALLOWED_SYMBOLS = [(48, 58), (65, 91), (97, 123)]  # 0-9, A-Z, a-z


def is_unique(short_id: str) -> bool:
    return not URLMap.query.filter_by(short=short_id).first()


def get_unique_short_id(id_length=6) -> str:
    buffer = []
    for _ in range(id_length):
        start, end = choice(ALLOWED_SYMBOLS)
        buffer.append(chr(randrange(start, end)))
    new_id = ''.join(buffer)

    if not is_unique(new_id):
        return get_unique_short_id()

    return new_id


def check_short_id(short_id: str) -> bool:
    if len(short_id) > 16:
        return False

    for char in short_id:
        is_ok = False

        for start, end in ALLOWED_SYMBOLS:
            if start <= ord(char) < end:
                is_ok = True

        if not is_ok:
            return False

    return True
