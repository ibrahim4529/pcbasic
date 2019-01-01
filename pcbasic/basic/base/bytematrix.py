"""
PC-BASIC - bytematrix.py
2D matrices of bytes

(c) 2018--2019 Rob Hagemans
This file is released under the GNU GPL version 3 or later.
"""

from binascii import hexlify, unhexlify

from ...compat import zip


class ByteMatrix(object):
    """2D byte matrix."""

    def __init__(self, width=0, height=0, data=0):
        """Create a new matrix."""
        self._width = width
        self._height = height
        if not width and not height:
            self._data = None
        elif isinstance(data, int):
            self._rows = [bytearray([data])*width for _ in range(self._height)]
        else:
            # assume iterable, TypeError if not
            data = list(data)
            if len(data) == 1:
                self._rows = [bytearray(data)*width for _ in range(self._height)]
            elif len(data) == height:
                assert len(data[0]) == width
                self._rows = [bytearray(_row) for _row in data]
            else:
                assert len(data) == height * width
                self._rows = [
                    bytearray(data[_offs : _offs+width])
                    for _offs in range(0, len(data), width)
                ]

    def __repr__(self):
        """Debugging representation."""
        hexreps = [''.join('\\x{:02x}'.format(_c) for _c in _row) for _row in self._rows]
        return "ByteMatrix({0._width}, {0._height}, [\n    '{1}' ])".format(
            self, "',\n    '".join(hexreps)
        )

    #def __str__(self):
    #    """Represent as string."""
    #    return '\n    ' + '\n    '.join(hexlify(bytes(_row)) for _row in self._rows)

    def __getitem__(self, index):
        """Extract items by [x, y] indexing or slicing or 1D index."""
        x, y = index
        if isinstance(y, slice):
            if isinstance(x, slice):
                return self._create_from_rows([_row[x] for _row in self._rows[y]])
            else:
                return self._create_from_rows([bytearray([_row[x]]) for _row in self._rows[y]])
        if isinstance(x, slice):
            return self._create_from_rows([self._rows[y][x]])
        return self._rows[y][x]

    def __setitem__(self, index, value):
        """Extract items by indexing or slicing."""
        x, y = index
        if isinstance(value, ByteMatrix):
            value = value._rows
        if isinstance(y, slice):
            for _dst, _src in zip(self._rows[y], value):
                _dst[x] = _src
        elif isinstance(x, slice):
            assert len(value) == 1
            self._rows[y][x] = value[0]
        else:
            self._rows[y][x] = value

    #def __len__(self):
    #    """Size in bytes."""
    #    return self._width * self._height

    @property
    def width(self):
        """Number of columns."""
        return self._width

    @property
    def height(self):
        """Number of rows."""
        return self._height

    @classmethod
    def _create_from_rows(cls, data):
        """Construct byte matrix from rows of bytearrays."""
        new = cls()
        new._height = len(data)
        new._width = len(data[0])
        new._rows = data
        assert len(set(len(_r) for _r in data)) == 1, 'ByteMatrix rows must all be same length'
        return new

    @classmethod
    def frompacked(cls, packed, height, items_per_byte=8):
        """Unpack from packed-bits representation."""
        width = items_per_byte * len(packed) // height
        unpacked = unpack_bytes(packed, items_per_byte)
        return cls._create_from_rows([
            unpacked[_offs : _offs+width]
            for _offs in range(0, len(unpacked), width)
        ])

    def packed(self, items_per_byte):
        """Pack into packed-bits representation."""
        joined = bytearray().join(self._rows)
        return pack_bytes(joined, items_per_byte)

    @classmethod
    def fromhex(cls, hex, height, items_per_byte=8):
        """Unpack from hex representation."""
        return cls.frompacked(unhexlify(hex), height, items_per_byte)

    def hex(self, items_per_byte=8):
        """Pack to hex representation."""
        return hexlify(self.packed(items_per_byte))

    def render(self, back, fore):
        """Set attributes on bit matrix."""
        return self._create_from_rows([
            _row.replace(b'\0', chr(back)).replace(b'\x01', chr(fore))
            for _row in self._rows
        ])

    def hextend(self, by_width, fill=0):
        """Extend width by given number of bytes."""
        new_row = bytearray([fill])*by_width
        return self._create_from_rows([_row + new_row for _row in self._rows])

    def vextend(self, by_height, fill=0):
        """Extend height by given number of bytes."""
        return self._create_from_rows(
            self._rows
            + [bytearray([fill])*self._width for _ in range(by_height)]
        )

    def hrepeat(self, times=1):
        """Multiply width by byte repetition (00 11 22 ...) ."""
        return self._create_from_rows([
            bytearray(_byte for _byte in _row for _ in range(times))
            for _row in self._rows
        ])


##############################################################################
# concatenation

def hstack(matrices):
    """Horizontally concatenate matrices."""
    matrices = list(matrices)
    return ByteMatrix._create_from_rows([
        bytearray().join(_rows)
        for _rows in zip(*(_mat._rows for _mat in matrices))
    ])

def vstack(matrices):
    """Vertically concatenate matrices."""
    return ByteMatrix._create_from_rows([
        _row for _mat in matrices for _row in _mat._rows
    ])


##############################################################################
# bytearray functions

def unpack_bytes(packed, items_per_byte):
    """Unpack from packed-bits representation."""
    bpp = 8 // items_per_byte
    mask = (1 << bpp) - 1
    shifts = [8 - bpp - _sh for _sh in range(0, 8, bpp)]
    return bytearray(
        (_byte >> _shift) & mask
        for _byte in packed
        for _shift in shifts
    )

def pack_bytes(unpacked, items_per_byte):
    """Pack into packed-bits representation."""
    bpp = 8 // items_per_byte
    mask = (1 << bpp) - 1
    shifts = [8 - bpp - _sh for _sh in range(0, 8, bpp)]
    packed_width = len(unpacked) // items_per_byte
    prepacked = [(_byte & mask) << _shift for _byte, _shift in zip(unpacked, shifts*packed_width)]
    return bytearray([
        sum(prepacked[_offs : _offs+items_per_byte])
        for _offs in range(0, len(prepacked), items_per_byte)
    ])
