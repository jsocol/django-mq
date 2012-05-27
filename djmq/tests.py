try:
    from django.db.query_utils import Q
except ImportError:
    from djmq._query_utils import Q

from djmq import _query_utils


def eq_(a, b, msg=None):
    message = msg or '%s != %s' % (a, b)
    assert a == b, message


if not hasattr(Q, '__eq__'):
    Q.__eq__ = _query_utils.__eq__
    Q.__ne__ = _query_utils.__ne__


from djmq.parser import parse_query


def test_empty_query():
    expect = Q()
    result = parse_query({})
    eq_(expect, result)


def test_single_query():
    expect = Q(a=1)
    result = parse_query({'a': 1})
    eq_(expect, result)


def test_and_query():
    expect = Q(a=1, b=2)
    result = parse_query({'a': 1, 'b': 2})
    eq_(expect, result)


def test_ordered_and_query():
    """The order of arguments shouldn't matter."""
    expect = Q(a=1, b=2)
    result = parse_query({'b': 2, 'a': 1})
    eq_(expect, result)


def test_or_query():
    expect = Q(a=1) | Q(b=2)
    result = parse_query({'$or': [{'a': 1}, {'b': 2}]})
    eq_(expect, result)


def test_and_or_query():
    expect = Q(a=1, b=2) | Q(c=3)
    input_ = {'$or': [{'a': 1, 'b':2}, {'c': 3}]}
    result = parse_query(input_)
    eq_(expect, result)


def test_not_query():
    expect = Q(a=1)
    expect.negate()
    result = parse_query({'$not': [{'a': 1}]})
    eq_(expect, result)


def test_or_not_query():
    a = Q(a=1)
    expect = Q(b=2) | ~a
    result = parse_query({'$or': [{'$not': [{'a': 1}]}, {'b': 2}]})
    eq_(expect, result)


def test_gt_query():
    expect = Q(a__gt=1)
    result = parse_query({'a': {'$gt': 1}})
    eq_(expect, result)


def test_lt_query():
    expect = Q(a__lt=3)
    result = parse_query({'a': {'$lt': 3}})
    eq_(expect, result)


def test_gt_lt_query():
    expect = Q(a__gt=3, a__lt=7)
    result = parse_query({'a': {'$gt': 3, '$lt': 7}})
    eq_(expect, result)


def test_lte_query():
    expect = Q(a__lte=3)
    result = parse_query({'a': {'$lte': 3}})
    eq_(expect, result)


def test_gte_query():
    expect = Q(a__gte=3)
    result = parse_query({'a': {'$gte': 3}})
    eq_(expect, result)
