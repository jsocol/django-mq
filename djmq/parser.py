import operator

try:
    from django.db.query_utils import Q
except ImportError:
    from _query_utils import Q


def parse_query(query):
    """Turns a MongoDB-style query dict into a Q object."""
    q = []
    iterator = getattr(query, 'items', query)
    if callable(iterator):
        iterator = iterator()
    for x in iterator:
        if isinstance(x, dict):
            k, v = x.items()[0]
        else:
            k, v = x[0], x[1]
        if k == '$or':
            or_ = parse_query(v)
            q.append(or_)
        else:
            q.append(Q((k, v)))

    return reduce(operator.and_, q)
