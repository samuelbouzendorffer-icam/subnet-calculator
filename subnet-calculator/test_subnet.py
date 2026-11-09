import unittest

import subnet


class TestSubnet(unittest.TestCase):
    def test_describe_host_address_inside_a_26(self):
        d = subnet.describe("192.168.1.130/26")
        self.assertEqual(d["network"], "192.168.1.128")
        self.assertEqual(d["netmask"], "255.255.255.192")
        self.assertEqual(d["wildcard"], "0.0.0.63")
        self.assertEqual(d["broadcast"], "192.168.1.191")
        self.assertEqual(d["first_host"], "192.168.1.129")
        self.assertEqual(d["last_host"], "192.168.1.190")
        self.assertEqual(d["usable_hosts"], 62)
        self.assertTrue(d["private"])

    def test_public_network(self):
        self.assertFalse(subnet.describe("8.8.8.0/24")["private"])

    def test_special_prefixes(self):
        self.assertEqual(subnet.describe("10.0.0.0/32")["usable_hosts"], 1)
        self.assertEqual(subnet.describe("10.0.0.0/31")["usable_hosts"], 2)
        self.assertEqual(subnet.describe("10.0.0.0/30")["usable_hosts"], 2)

    def test_split(self):
        self.assertEqual(subnet.split("10.0.0.0/24", 26),
                         ["10.0.0.0/26", "10.0.0.64/26", "10.0.0.128/26", "10.0.0.192/26"])

    def test_split_invalid_prefix(self):
        with self.assertRaises(ValueError):
            subnet.split("10.0.0.0/24", 24)

    def test_contains(self):
        self.assertTrue(subnet.contains("192.168.0.0/16", "192.168.42.7"))
        self.assertFalse(subnet.contains("192.168.0.0/16", "192.169.0.1"))

    def test_prefix_for_hosts(self):
        self.assertEqual(subnet.prefix_for_hosts(50), 26)   # 62 machines possibles
        self.assertEqual(subnet.prefix_for_hosts(62), 26)
        self.assertEqual(subnet.prefix_for_hosts(63), 25)   # 126 machines possibles
        self.assertEqual(subnet.prefix_for_hosts(254), 24)
        self.assertEqual(subnet.prefix_for_hosts(2), 31)

    def test_ipv6_refused(self):
        with self.assertRaises(ValueError):
            subnet.describe("2001:db8::/32")


if __name__ == "__main__":
    unittest.main()
