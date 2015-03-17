from binary import BinaryStream
import struct

TAG_FINISH = 0
TAG_STR_BYTE = 1
TAG_STR_SHORT = 2
TAG_STR_INT = 3
TAG_STR_LONG = 4
TAG_STR_FLOAT = 5
TAG_STR_DOUBLE = 6
TAG_STR_BYTEARRAY = 7
TAG_STR_STRING = 8
TAG_STR_FLOAT3 = 9
TAG_STR_INT3 = 10
TAG_STR_BYTE3 = 11
TAG_STR_LIST = 12
TAG_STR_STRUCT = 13
TAG_STR_SERIAL = 14

TAG_RGBA = 241
TAG_UNK = 242
TAG_STRUCT = 243
TAG_LIST = 244
TAG_BYTE3 = 245
TAG_INT3 = 246
TAG_FLOAT3 = 247
TAG_STRING = 248
TAG_BYTEARRAY = 249
TAG_DOUBLE = 250
TAG_FLOAT = 251
TAG_LONG = 252
TAG_INT = 253
TAG_SHORT = 254
TAG_BYTE = 255


class TagParser:
    """
    Test
    """

    def __init__(self, stream):
        self.stream = stream

    def read(self):
        all_tags = []
        tag = self.stream.readUChar()
        while tag != TAG_FINISH:
            item = self.parse_tag(tag)
            try:
                tag = self.stream.readUChar()
            except struct.error:  # Missing Tag Finish Char
                tag = TAG_FINISH
            all_tags.append(item)
        return all_tags

    def parse_bytearray(self):
        l = self.stream.readInt32()
        data = []
        for i in xrange(l):
            data.append(self.stream.readChar())
        return data

    def parse_list(self):
        data = []
        next_tag = self.stream.readUChar()
        l = self.stream.readInt32()
        for i in xrange(l):
            data.append(self.parse_list_tag(next_tag))
        return data

    def parse_list_tag(self, tag):
        if tag == TAG_STR_BYTE:
            return self.stream.readChar()
        elif tag == TAG_STR_SHORT:
            return self.stream.readInt16()
        elif tag == TAG_STR_INT:
            return self.stream.readInt32()
        elif tag == TAG_STR_LONG:
            return self.stream.readInt64()
        elif tag == TAG_STR_FLOAT:
            return self.stream.readFloat()
        elif tag == TAG_STR_DOUBLE:
            return self.stream.readDouble()
        elif tag == TAG_STR_BYTEARRAY:
            return self.parse_bytearray()
        elif tag == TAG_STR_STRING:
            return self.stream.readString()
        elif tag == TAG_STR_FLOAT3:
            return self.stream.readVec3F()
        elif tag == TAG_STR_INT3:
            return self.stream.readVec3Int32()
        elif tag == TAG_STR_BYTE3:
            return self.stream.readVec3Char()
        else:
            print 'unrecognized tag type while parsing list tag'
            return None

    def parse_struct(self):
        next_tag = self.stream.readUChar()
        # data = {}
        data = []
        while next_tag != TAG_FINISH:
            item = self.parse_tag(next_tag)
            data.append(item)
            next_tag = self.stream.readUChar()
        return data

    def parse_serial(self):
        data = ''
        next_bytes = self.stream.readBytes(11)
        while next_bytes != '\b\0\brealname':
            data += self.stream.readByte()
            next_bytes = self.stream.readBytes(11)
        return data

    def parse_tag(self, tag):
        if tag == TAG_STR_BYTE:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readChar()
            }

        elif tag == TAG_BYTE:
            return self.stream.readChar()

        elif tag == TAG_STR_SHORT:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readInt16()
            }

        elif tag == TAG_SHORT:
            return self.stream.readInt16()

        elif tag == TAG_STR_INT:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readInt32()
            }

        elif tag == TAG_INT:
            return self.stream.readInt32()

        elif tag == TAG_STR_LONG:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readInt64()
            }

        elif tag == TAG_LONG:
            return self.stream.readInt64()

        elif tag == TAG_STR_FLOAT:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readFloat()
            }

        elif tag == TAG_FLOAT:
            return self.stream.readFloat()

        elif tag == TAG_STR_DOUBLE:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readDouble()
            }

        elif tag == TAG_DOUBLE:
            return self.stream.readDouble()

        elif tag == TAG_STR_BYTEARRAY:
            return {
                'name': self.stream.readString(),
                'value': self.parse_bytearray()
            }

        elif tag == TAG_BYTEARRAY:
            return self.parse_bytearray()

        elif tag == TAG_STR_STRING:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readString()
            }

        elif tag == TAG_STRING:
            return self.stream.readString()

        elif tag == TAG_STR_FLOAT3:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readVec3F()
            }

        elif tag == TAG_FLOAT3:
            return self.stream.readVec3F()

        elif tag == TAG_STR_INT3:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readVec3Int32()
            }

        elif tag == TAG_INT3:
            return self.stream.readVec3Int32()

        elif tag == TAG_STR_BYTE3:
            return {
                'name': self.stream.readString(),
                'value': self.stream.readVec3Char()
            }

        elif tag == TAG_BYTE3:
            return self.stream.readVec3Char()

        elif tag == TAG_STR_LIST:
            return {
                'name': self.stream.readString(),
                'value': self.parse_list()
            }

        elif tag == TAG_LIST:
            return self.parse_list()

        elif tag == TAG_STR_STRUCT:
            return {
                'name': self.stream.readString(),
                'value': self.parse_struct()
            }

        elif tag == TAG_STRUCT:
            return self.parse_struct()

        elif tag == TAG_STR_SERIAL:
            return {
                'name': self.stream.readString(),
                'value': self.parse_serial()
            }

        elif tag == TAG_RGBA:
            return self.stream.readVec4F()

        elif tag == TAG_UNK:
            return self.stream.readBytes(16)

        else:
            print 'unrecognized tag type'
