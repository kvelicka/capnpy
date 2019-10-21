import six
from capnpy.schema import CodeGeneratorRequest, Node
from capnpy.annotate import Options
from capnpy.compiler.module import ModuleGenerator

# main API entry point for end users
def get_reflection_data(module):
    try:
        return module._reflection_data
    except AttributeError:
        raise ValueError("Reflection data not found in module %s" %
                         module)


class ReflectionData(object):

    # subclasses are supposed to fill these fields accordingly
    request_data = None
    default_options_data = None
    pyx = False

    # ModuleGenerator, initialized lazily
    _m = None
    @property
    def m(self):
        if self._m is not None:
            return self._m
        #
        request = CodeGeneratorRequest.loads(self.request_data)
        default_options = Options.loads(self.default_options_data)
        self._m = ModuleGenerator(request,
                                  pyx=self.pyx,
                                  standalone=True,
                                  default_options=default_options,
                                  capnproto_version=None)
        return self._m

    @property
    def allnodes(self):
        return self.m.allnodes

    def get_node(self, obj=None):
        """
        Get the schema.Node corresponding to obj. Obj can be either:

            - an integer representing the node ID

            - a capnpy-generated object which has a __capnpy_id__ attribute,
              such as modules, types or annotations
        """
        if isinstance(obj, six.integer_types):
            id = obj
        else:
            id = obj.__capnpy_id__
        return self.m.allnodes[id]

    def get_annotation(self, entity, anncls):
        ann = self._get_annotation(entity, anncls)
        if ann:
            return ann.annotation.value.as_pyobj()
        raise KeyError(anncls.__name__)

    def has_annotation(self, entity, anncls):
        ann = self._get_annotation(entity, anncls)
        return bool(ann)

    def _get_annotation(self, entity_or_node, anncls):
        if isinstance(entity_or_node, Node):
            node = entity_or_node
        else:
            node = self.get_node(entity_or_node)
        return self.m.has_annotation(node, anncls)

    def field_name(self, f):
        """
        Return the Python-level name of the given capnproto field, as generated by
        the compiler
        """
        return self.m.py_field_name(f)
