import operator

try:
    from django.db.query_utils import Q
except ImportError:
    from _query_utils import Q


def parse_query(query, o=None):
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
            or_ = parse_query(v, operator.or_)
            q.append(or_)
        elif k == '$not':
            not_ = parse_query(v)
            not_.negate()
            q.append(not_)
        else:
            if hasattr(x, 'keys') and len(x.keys()) > 1:
                q.append(parse_query(x))
            else:
                if isinstance(v, dict):
                    for comp, value in v.items():
                        if comp == '$gt':
                            q.append(Q(**{'%s__gt' % k: value}))
                        elif comp == '$lt':
                            q.append(Q(**{'%s__lt' % k: value}))
                else:
                    q.append(Q((k, v)))

    if q:
        return reduce(o or operator.and_, q)
    return Q()
