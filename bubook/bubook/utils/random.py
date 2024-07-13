from random import choice


def random_int(length: int) -> str:
    return ''.join(choice('1234567890') for _ in range(length))
