import unittest
import ups_parsers

class TestStringMethods(unittest.TestCase):

    def test_parse_pwrstat(self):
        lines = ups_parsers.read_all_lines("tests/pwrstat.output")
        info = ups_parsers.parse_pwrstat(lines)
        self.assertEqual(info["ups_usage_pct"], 12.0)
        self.assertEqual(info["ups_usage_watt"], 120.0)
        self.assertEqual(info["ups_time_left"], 61.0)
        self.assertEqual(info["ups_utility_volts"], 119.0)
        self.assertEqual(info["ups_battery_volts"], None)
        self.assertEqual(info["ups_battery_capacity"], 100.0)
        self.assertEqual(info["ups_state"], "line")

    def test_parse_apcaccess(self):
        lines = ups_parsers.read_all_lines("tests/apcaccess.output")
        info = ups_parsers.parse_apcaccess(lines)
        self.assertEqual(info["ups_usage_pct"], 9.0)
        self.assertEqual(info["ups_usage_watt"], None)
        self.assertEqual(info["ups_time_left"], 82.3)
        self.assertEqual(info["ups_utility_volts"], 122.0)
        self.assertEqual(info["ups_battery_volts"], 13.5)
        self.assertEqual(info["ups_battery_capacity"], 100.0)
        self.assertEqual(info["ups_state"], "line")

if __name__ == '__main__':
    unittest.main()