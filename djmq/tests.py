from nose.tools import eq_

try:
    from django.db.query_utils import Q
except ImportError:
    from djmq._query_utils import Q

from djmq.parser import parse_query


def fix_children(l):
    for i, x in enumerate(l):
        if isinstance(x, dict):
            l[i] = x.items()[0]


def compare_query(a, b, msg=None):
    """Compare two Q objects, since Q.__eq__ doesn't exist."""
    ad, bd = a.__dict__, b.__dict__
    fix_children(ad['children'])
    fix_children(bd['children'])
    eq_(ad, bd, msg or '%r != %r' % (a, b))


def test_single_query():
    expect = Q(a=1)
    result = parse_query({'a': 1})
    compare_query(expect, result)


def test_and_query():
    expect = Q(a=1, b=2)
    result = parse_query({'a': 1, 'b': 2})
    compare_query(expect, result)


def test_or_query():
    expect = Q(a=1) | Q(b=2)
    result = parse_query({'$or': [{'a': 1}, {'b': 2}]})
    compare_query(expect, result)


def test_and_or_query():
    expect = Q(a=1, b=2) | Q(c=3)
    input_ = {'$or': [{'a': 1, 'b':2}, {'c': 3}]}
    result = parse_query(input_)
    compare_query(expect, result)
