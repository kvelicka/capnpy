import struct
import math
from capnpy.unpack import unpack_primitive

def test_unpack_primitive_ints():
    buf = '\xff' * 8
    assert unpack_primitive(ord('b'), buf, 0) == -1
    assert unpack_primitive(ord('h'), buf, 0) == -1
    assert unpack_primitive(ord('i'), buf, 0) == -1
    assert unpack_primitive(ord('q'), buf, 0) == -1
    #
    assert unpack_primitive(ord('B'), buf, 0) == (1 <<  8) - 1
    assert unpack_primitive(ord('H'), buf, 0) == (1 << 16) - 1
    assert unpack_primitive(ord('I'), buf, 0) == (1 << 32) - 1
    assert unpack_primitive(ord('Q'), buf, 0) == (1 << 64) - 1
    
def test_unpack_primitive_floats():
    buf = struct.pack('f', math.pi)
    assert unpack_primitive(ord('f'), buf, 0) == struct.unpack('f', buf)[0]
    #
    buf = struct.pack('d', math.pi)
    assert unpack_primitive(ord('d'), buf, 0) == struct.unpack('d', buf)[0]
