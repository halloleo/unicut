"""
The truncate functions
"""

def truncate_by_concating(s, max_bytes):
    """
    Ensure that the UTF-8 encoding of a string has not more than
    max_bytes bytes
    :param s: The string
    :param max_bytes: Maximal number of bytes
    :return: The cut string
    """
    def len_as_bytes(s):
        return len(s.encode(errors='replace'))

    if len_as_bytes(s) <= max_bytes:
        return s

    res = ""
    for c in s:
        old = res
        res += c
        if len_as_bytes(res) > max_bytes:
            res = old
            break
    return res


def truncate_by_backing_up_bytes(s, max_bytes):
    """
    Ensure that the UTF-8 encoding of a string has not more than
    max_bytes bytes
    :param s: The string
    :param max_bytes: Maximal number of bytes
    :return: The cut string
    """
    def safe_b_of_i(b, i):
        try:
            return b[i]
        except IndexError:
            return 0

    # Edge cases
    if s == '' or max_bytes < 1:
        return ''

    # cut it twice to avoid encoding potentially GBs of `s` just to get e.g. 10 bytes?
    b = s[:max_bytes].encode('utf-8')[:max_bytes]

    if b[-1] & 0b10000000:
        last_11xxxxxx_index = [i for i in range(-1, -5, -1)
                               if safe_b_of_i(b,i) & 0b11000000 == 0b11000000][0]
        # note that last_11xxxxxx_index is negative

        last_11xxxxxx = b[last_11xxxxxx_index]
        if not last_11xxxxxx & 0b00100000:
            last_char_length = 2
        elif not last_11xxxxxx & 0b0010000:
            last_char_length = 3
        elif not last_11xxxxxx & 0b0001000:
            last_char_length = 4

        if last_char_length > -last_11xxxxxx_index:
            # remove the incomplete character
            b = b[:last_11xxxxxx_index]

    return b.decode('utf-8')


# List of the truncate functions
truncate_funcs = [truncate_by_concating,
                  truncate_by_backing_up_bytes,
                  ]
