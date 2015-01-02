class Primitive(object):

    def __init__(self, offset, type):
        self.offset = offset
        self.type = type

    def __get__(self, blob, cls):
        if blob is None:
            return self
        return blob._read_primitive(self.offset, self.type)

    def __repr__(self):
        return '<Field +%d: Primitive, type=%s>' % (self.offset, self.type.name)
        

class String(object):

    def __init__(self, offset):
        self.offset = offset

    def __get__(self, blob, cls):
        if blob is None:
            return self
        return blob._read_string(self.offset)

    def __repr__(self):
        return '<Field +%d: String>' % (self.offset,)


class List(object):

    def __init__(self, offset, listcls, item_type):
        self.offset = offset
        self.listcls = listcls
        self.item_type = item_type

    def __get__(self, blob, cls):
        if blob is None:
            return self
        return blob._read_list(self.offset, self.listcls, self.item_type)

    def __repr__(self):
        return ('<Field +%d: List, listcls=%s, item_type=%s>' %
                (self.offset, self.listcls.__name__, self.item_type.name))


class Struct(object):

    def __init__(self, offset, structcls):
        self.offset = offset
        self.structcls = structcls

    def __get__(self, blob, cls):
        if blob is None:
            return self
        return blob._read_struct(self.offset, self.structcls)

    def __repr__(self):
        return ('<Field +%d: Struct, structcls=%s>' %
                (self.offset, self.structcls.__name__))


class Enum(object):

    def __init__(self, offset, enumcls):
        self.offset = offset
        self.enumcls = enumcls

    def __get__(self, blob, cls):
        if blob is None:
            return self
        return blob._read_enum(self.offset, self.enumcls)

    def __repr__(self):
        return ('<Field +%d: Enum, enumcls=%s>' %
                (self.offset, self.enumcls.__name__))


class Union(object):

    def __init__(self, tag, field):
        self.tag = tag
        self.field = field

    def __get__(self, blob, cls):
        if blob is None:
            return self
        blob._ensure_union(self.tag)
        return self.field.__get__(blob, cls)

    def __repr__(self):
        return '<Union %s: %s>' % (self.tag.name, self.field)


class Group(object):

    def __init__(self, groupcls):
        self.groupcls = groupcls

    def __get__(self, blob, cls):
        if blob is None:
            return self
        return blob._read_group(self.groupcls)

    def __repr__(self):
        return '<Group %s>' % self.groupcls.__name__
