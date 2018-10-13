import random
import string


# default character set from which to generate random strings
_DEFAULT = string.ascii_lowercase + string.ascii_uppercase + string.digits


def generate_random_string(length, letters=_DEFAULT):
    """Generates a cryptographically safe random string.
    """
    assert letters, 'Character set from which to generate string required'
    chars = [random.SystemRandom().choice(letters) for _ in range(length)]
    return ''.join(chars)
