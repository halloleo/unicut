#!/usr/bin/env python3
"""
Time the execution of the truncate functions
"""
import timeit
import sys

from truncate import truncate_funcs, truncate_by_concating, truncate_by_backing_up_bytes


TESTSTRS = {
'SHORT_ASCII': 'Dog',
'LONG_ASCII': 'The quick brown fox jumps over the lazy dog.',
'SHORT_UNICODE': '\U0001F600\u2014\xD6',
'LONG_UNICODE': 'The\U0001F600quick\u2014brown\xD6fox\U0001F600jumps\u2014over\xD6the\U0001F600lazy\u2014dog.',
    }

TIMEIT_SETUP = 'import timeit_truncate as tt'


def time_executions_A(uncut=False):
    """
    Time executions via timeit module level calls
    """
    for strname in ['SHORT_UNICODE',
                    'LONG_UNICODE']:  # only unicode strings
        for truncate in truncate_funcs:
            cut_txt = "UNCUT" if uncut else "CUT at len-2"
            cut_len = sys.maxsize if uncut else len(TESTSTRS[strname])-2
            print(f"Time '{truncate.__name__}' with {strname} string {cut_txt}")
            stmt = f"tt.{truncate.__name__}(tt.TESTSTRS['{strname}'], {cut_len})"
            timeit.main(['-u', 'usec', '-n', '100000', '-s', TIMEIT_SETUP, stmt])


if __name__ == '__main__':
    time_executions = time_executions_A

    print("--- Timeings WITHOUT cutting the strings ---")
    time_executions(uncut=True)

    print("\n--- Timeings WITH cutting the strings (at len-2) ---")
    time_executions(uncut=False)


