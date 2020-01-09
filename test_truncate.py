"""
Tests for truncate functions
"""
import sys
import pytest
import hypothesis as ht
import hypothesis.strategies as htst

from truncate import truncate_funcs


@pytest.mark.parametrize('truncate', truncate_funcs)
class Test_manual():
    def test_ascii_uncut(self, truncate):
        s = "A normal string"
        assert s == truncate(s, sys.maxsize)

    def test_ascii_cut(self, truncate):
        s = "A normal string"
        max_len = 8
        assert s[0:max_len] == truncate(s, max_len)

    def test_unicode_uncut(self, truncate):
        s = "NO。121 TUCHENKONG VILLAGE"
        assert s == truncate(s, sys.maxsize)

    def test_unicode_cut(self, truncate):
        s = "NO。121 TUCHENKONG VILLAGE"
        max_bytes = 12
        max_chars = 10
        assert s[0:max_chars] == truncate(s, max_bytes)


#
# hypothesis stuff
#
ascii_abc = [ chr(x) for x in range(128) ]

ht.settings.register_profile('base', max_examples=200, verbosity=ht.Verbosity.verbose)
ht.settings.load_profile('base')

@pytest.mark.parametrize('truncate', truncate_funcs)
class Test_propbased():
    @ht.given(s=htst.text(alphabet=ascii_abc))
    def test_ascii_uncut(self, s, truncate):
        assert s == truncate(s, sys.maxsize)

    @ht.given(s=htst.text(alphabet=ascii_abc), max_len=htst.integers(min_value=0))
    def test_ascii_cut(self, s, max_len, truncate):
        assert s[0:max_len] == truncate(s, max_len)

    @ht.given(s=htst.text())
    def test_unicode_uncut(self, s, truncate):
        assert s == truncate(s, sys.maxsize)

    @ht.given(s=htst.text(), max_len=htst.integers(min_value=0, max_value=10000),)
    def test_unicode_cut(self, s, max_len, truncate):
        t = truncate(s, max_len)
        assert s.startswith(t)


@ht.given(s=htst.text(), max_len=htst.integers(min_value=0, max_value=10000), )
def test_propbased_assert_each_other(s, max_len):
    assert truncate_by_concating(s, max_len) == truncate_by_backing_up_bytes(s, max_len)
