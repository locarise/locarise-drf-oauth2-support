

def sane_repr(*attrs):
    if 'uid' not in attrs and 'pk' not in attrs:
        attrs = ('uid',) + attrs

    def _repr(self):
        cls = type(self).__name__

        pairs = ('%s=%s' % (a, repr(getattr(self, a, None)))
                 for a in attrs)

        return u'<%s at 0x%x: %s>' % (cls, id(self), ', '.join(pairs))

    return _repr
