import random
import string
import datetime


def make_id(n_char=12):
    use_chars = string.ascii_letters + string.digits
    t = datetime.datetime.now()
    t.strftime("%Y%m%d_%H%M%S")
    return f'{t.strftime("%Y%m%d_%H%M%S")}_{"".join(random.choice(use_chars) for _ in range(n_char))}'
