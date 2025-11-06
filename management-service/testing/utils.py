__all__ = ("get_random_string",)

import random
import string


def get_random_string(length: int = 8) -> str:
    """Возвращает случайную строку из букв ascii_letters заданной длины."""
    return "".join(
        random.choices(
            string.ascii_letters,
            k=length,
        ),
    )
