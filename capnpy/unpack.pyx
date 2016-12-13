from libc.stdint cimport (int8_t, uint8_t, int16_t, uint16_t,
                          uint32_t, int32_t, int64_t, uint64_t, INT64_MAX)
from cpython.string cimport (PyString_GET_SIZE, PyString_AS_STRING,
                             PyString_CheckExact)

cdef extern from "Python.h":
    int PyByteArray_CheckExact(object o)
    char* PyByteArray_AS_STRING(object o)
    Py_ssize_t PyByteArray_GET_SIZE(object o)

cdef char* as_cbuf(object buf, Py_ssize_t* length) except NULL:
    # PyString_AS_STRING seems to be faster than relying of cython's own logic
    # to convert bytes to char*
    cdef bytes bytes_buf
    cdef bytearray ba_buf
    if PyString_CheckExact(buf):
        bytes_buf = buf
        length[0] = PyString_GET_SIZE(bytes_buf)
        return PyString_AS_STRING(bytes_buf)
    elif PyByteArray_CheckExact(buf):
        ba_buf = buf
        length[0] = PyByteArray_GET_SIZE(ba_buf)
        return PyByteArray_AS_STRING(ba_buf)
    else:
        raise TypeError

cdef checkbound(int size, Py_ssize_t length, int offset):
    if offset + size > length:
        raise IndexError('Offset out of bounds: %d' % offset)

cpdef unpack_primitive(char ifmt, object buf, int offset):
    cdef char* cbuf
    cdef void* valueaddr
    cdef uint64_t uint64_value
    cdef Py_ssize_t length = 0
    #
    if offset < 0:
        raise IndexError('Offset out of bounds: %d' % offset)
    cbuf = as_cbuf(buf, &length)
    valueaddr = cbuf + offset
    if ifmt == 'q':
        checkbound(8, length, offset)
        return (<int64_t*>valueaddr)[0]
    elif ifmt == 'Q':
        # if the value is small enough, it returns a python int. Else, a
        # python long
        checkbound(8, length, offset)
        uint64_value = (<uint64_t*>valueaddr)[0]
        if uint64_value <= INT64_MAX:
            return <int64_t>uint64_value
        else:
            return uint64_value
    elif ifmt == 'd':
        checkbound(8, length, offset)
        return (<double*>valueaddr)[0]
    elif ifmt == 'f':
        checkbound(4, length, offset)
        return (<float*>valueaddr)[0]
    elif ifmt == 'i':
        checkbound(4, length, offset)
        return (<int32_t*>valueaddr)[0]
    elif ifmt == 'I':
        checkbound(4, length, offset)
        return (<uint32_t*>valueaddr)[0]
    elif ifmt == 'h':
        checkbound(2, length, offset)
        return (<int16_t*>valueaddr)[0]
    elif ifmt == 'H':
        checkbound(2, length, offset)
        return (<uint16_t*>valueaddr)[0]
    elif ifmt == 'b':
        checkbound(1, length, offset)
        return (<int8_t*>valueaddr)[0]
    elif ifmt == 'B':
        checkbound(1, length, offset)
        return (<uint8_t*>valueaddr)[0]
    #
    raise ValueError('unknown fmt %s' % chr(ifmt))


cpdef long unpack_int64(object buf, int offset):
    cdef char* cbuf
    cdef void* valueaddr
    cdef Py_ssize_t length = 0
    #
    if offset < 0:
        raise IndexError('Offset out of bounds: %d' % offset)
    cbuf = as_cbuf(buf, &length)
    valueaddr = cbuf + offset
    checkbound(8, length, offset)
    return (<int64_t*>valueaddr)[0]

cpdef long unpack_int16(object buf, int offset):
    cdef char* cbuf
    cdef void* valueaddr
    cdef Py_ssize_t length = 0
    #
    if offset < 0:
        raise IndexError('Offset out of bounds: %d' % offset)
    cbuf = as_cbuf(buf, &length)
    valueaddr = cbuf + offset
    checkbound(2, length, offset)
    return (<int16_t*>valueaddr)[0]

cpdef long unpack_uint32(object buf, int offset):
    cdef char* cbuf
    cdef void* valueaddr
    cdef Py_ssize_t length = 0
    #
    if offset < 0:
        raise IndexError('Offset out of bounds: %d' % offset)
    cbuf = as_cbuf(buf, &length)
    valueaddr = cbuf + offset
    checkbound(4, length, offset)
    return (<uint32_t*>valueaddr)[0]
