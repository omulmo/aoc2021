#! /usr/bin/env python3
from operator import mul
from functools import reduce
import sys

class BitStream:
    def __init__(self, string, string_is_hex=True):
        if string_is_hex:
            nbits = 4 * len(string)
            bigint = int(string,base=16)
            string = f'{bigint:0{nbits}b}'
        self.string = string
        self.pos = 0

    def length(self):
        return len(self.string) - self.pos

    def read(self, count=1):
        if self.pos >= len(self.string):
            return ''
        x = self.string[self.pos:self.pos+count]
        self.pos += count
        return x

    def readInt(self):
        bits, again = '', True
        while again:
            again = self.read() == '1'
            bits += self.read(4)
        return int(bits,2)


class Packet:
    def __init__(self, bitstream):
        self.version = int(bitstream.read(3),2)
        self.type = int(bitstream.read(3),2)
        self.value = None
        self.subpackets = []
        if self.type == 4:
            self.value = bitstream.readInt()
        else:
            if bitstream.read()=='0':
                length = int(bitstream.read(15), 2)
                substream = BitStream(bitstream.read(length), string_is_hex=False)
                while substream.length() > 0:
                    self.subpackets.append(Packet(substream))
            else:
                n = int(bitstream.read(11), 2)
                for i in range(n):
                    self.subpackets.append(Packet(bitstream))

    def eval(self):
        generator = (p.eval() for p in self.subpackets)
        if self.type == 0:
            return sum(generator)
        elif self.type == 1:
            return reduce(mul, generator)
        elif self.type == 2:
            return reduce(min, generator)
        elif self.type == 3:
            return reduce(max, generator)
        elif self.type == 4:
            return self.value
        elif self.type == 5:
            a,b = generator
            return 1 if a > b else 0
        elif self.type == 6:
            a,b = generator
            return 1 if a < b else 0
        elif self.type == 7:
            a,b = generator
            return 1 if a == b else 0
        else:
            raise Exception


def sum_of_packet_versions(hex_string):
    packets = [ Packet(BitStream(hex_string)) ]
    count = 0
    while len(packets)>0:
        p = packets.pop(0)
        count += p.version
        packets.extend(p.subpackets)
    return count


if __name__=='__main__':
    mode = '1' if len(sys.argv)<2 else sys.argv[1]
    hex_string = sys.stdin.readline().strip()

    if mode == '1':
        print(sum_of_packet_versions(hex_string))
    else:
        print(Packet(BitStream(hex_string)).eval())
