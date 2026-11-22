#!/usr/bin/env python3
# -- coding: utf-8 --
"""Command-line entry-point tests."""

# Imports
import subprocess
import sys
import unittest


class CliTests(unittest.TestCase):
    def test_help(self):
        result = subprocess.run(
            [sys.executable, "-m", "ntdsdotsqlite.__main__", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NTDS.DIT file", result.stdout)
        self.assertIn("--system", result.stdout)


if __name__ == "__main__":
    unittest.main()
