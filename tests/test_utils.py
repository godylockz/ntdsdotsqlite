#!/usr/bin/env python3
# -- coding: utf-8 --
"""Tests for the SQLite schema and NTDS value conversions."""

# Imports
import sqlite3
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from ntdsdotsqlite.utils import (
    compute_links,
    create_database,
    escape_dn_chars,
    hundredns_to_datetime,
    raw_to_guid,
    raw_to_sid,
)


class _LinkTable:
    def records(self):
        return [
            {"link_DNT": 101, "backlink_DNT": 501},
            {"link_DNT": 102, "backlink_DNT": 501},
            {"link_DNT": 103, "backlink_DNT": 502},
        ]


class _EseDatabase:
    def table(self, name):
        if name != "link_table":
            raise AssertionError(name)
        return _LinkTable()


class UtilsTests(unittest.TestCase):
    def test_create_database_creates_expected_tables(self):
        with tempfile.TemporaryDirectory() as directory:
            database_path = Path(directory) / "ntds.sqlite"
            create_database(database_path)

            with sqlite3.connect(database_path) as database:
                tables = {
                    row[0]
                    for row in database.execute(
                        "SELECT name FROM sqlite_master WHERE type = ?",
                        ("table",),
                    )
                }

        self.assertEqual(
            tables,
            {
                "containers",
                "domain_dns",
                "domains",
                "groups",
                "machine_accounts",
                "organizational_units",
                "trusted_domains",
                "user_accounts",
            },
        )

    def test_raw_to_guid(self):
        raw = bytes.fromhex("78563412bc9af0de1122334455667788")
        self.assertEqual(raw_to_guid(raw), "12345678-9abc-def0-1122-334455667788")

    def test_raw_to_sid(self):
        raw = bytes.fromhex("010400000000000515000000200000003000000044332211")
        self.assertEqual(raw_to_sid(raw), "S-1-5-21-32-48-287454020")

    def test_raw_to_sid_rejects_truncated_input(self):
        with self.assertRaisesRegex(ValueError, "truncated"):
            raw_to_sid(bytes.fromhex("010200000000000515000000"))

    def test_hundredns_epoch(self):
        self.assertEqual(hundredns_to_datetime(0), datetime(1601, 1, 1))

    def test_escape_dn_chars(self):
        self.assertEqual(escape_dn_chars(" #Ops, East "), "\\ #Ops\\, East\\ ")

    def test_compute_links(self):
        self.assertEqual(
            compute_links(_EseDatabase()),
            {501: [101, 102], 502: [103]},
        )


if __name__ == "__main__":
    unittest.main()
