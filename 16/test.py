#! /usr/bin/env python3

import unittest
from star import sum_of_packet_versions, Packet, BitStream

class Test1(unittest.TestCase):
    def test1(self):
        self.assertEqual(16, sum_of_packet_versions('8A004A801A8002F478'))
    def test2(self):
        self.assertEqual(12, sum_of_packet_versions('620080001611562C8802118E34'))
    def test3(self):
        self.assertEqual(23, sum_of_packet_versions('C0015000016115A2E0802F182340'))
    def test4(self):
        self.assertEqual(31, sum_of_packet_versions('A0016C880162017C3686B18A3D4780'))


class Test2(unittest.TestCase):
    def test1(self):
        self.assertEqual(3, Packet(BitStream('C200B40A82')).eval())
        self.assertEqual(54, Packet(BitStream('04005AC33890')).eval())
        self.assertEqual(7, Packet(BitStream('880086C3E88112')).eval())
        self.assertEqual(9, Packet(BitStream('CE00C43D881120')).eval())
        self.assertEqual(1, Packet(BitStream('D8005AC2A8F0')).eval())
        self.assertEqual(0, Packet(BitStream('F600BC2D8F')).eval())
        self.assertEqual(0, Packet(BitStream('9C005AC2F8F0')).eval())
        self.assertEqual(1, Packet(BitStream('9C0141080250320F1802104A08')).eval())


if __name__=='__main__':
    unittest.main()
