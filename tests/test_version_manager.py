"""Focused regression tests for the reusable core."""

import unittest

from version_manager.versioning import VersionCalculator


class VersionCalculatorTests(unittest.TestCase):
    def test_bumps_semantic_versions(self):
        self.assertEqual(VersionCalculator.bump("1.2.3", "patch"), "1.2.4")
        self.assertEqual(VersionCalculator.bump("1.2.3", "minor"), "1.3.0")
        self.assertEqual(VersionCalculator.bump("1.2.3", "major"), "2.0.0")

    def test_accepts_v_tag_format(self):
        self.assertEqual(VersionCalculator.validate("v3.4.5"), "3.4.5")


if __name__ == "__main__":
    unittest.main()
