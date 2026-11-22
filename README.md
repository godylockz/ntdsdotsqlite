# NTDS.Sqlite

This software can be used either directly as a CLI utility or as a library to get an SQLite database from an NTDS.DIT one. Encrypted bits can be decrypted if the associated system hive is provided altogether.

This maintained fork is an offline analysis companion to NetExec and Impacket,
not a NetExec module. Use NetExec or Impacket to acquire or dump authorized
directory data, then use this tool when the relationships need to be queried as
SQL. If only credential material is needed, NetExec and `secretsdump` are the
simpler path.

# Installation

`python -m pip install "git+https://github.com/godylockz/ntdsdotsqlite.git"`

Python 3.10 through 3.14 are supported. Python 3.15 is temporarily excluded
because the current stable `dissect.cstruct` release uses regular-expression
behavior removed in Python 3.15. The cap can be removed after a compatible
stable release is available.

# Usage

`ntdsdotsqlite NTDS.DIT --system SYSTEM -o NTDS.sqlite`

The `SYSTEM` hive is optional. Without it, encrypted credential fields remain
encrypted in the SQLite output while directory relationships are still parsed.

```
usage: NTDS.sqlite [-h] [--system SYSTEM] -o OUTFILE NTDS

This tool helps dumping NTDS.DIT file to an SQLite database

positional arguments:
  NTDS                  The NTDS.DIT file

optional arguments:
  -h, --help            show this help message and exit
  --system SYSTEM       The SYSTEM hive to decrypt hashes. If not provided, hashes will be encrypted inside the sqlite database.
  -o OUTFILE, --outfile OUTFILE
                        The sqlite database. Example : NTDS.sqlite
```

# SQL model

The SQL model is described in the `sql_model.md` file in this repository. Basicaly, not all objects are extracted (at all), but the following are retrieved as of today : domain object, user accounts, machine accounts, groups, organizational units and containers. I thought these would be the most useful. If you need more object classes to be extracted or additional attributes, feel free to open an issue or a pull request !

# Performances

Performances can be a bit low for huge NTDS files. The whole NTDS is not stored in memory to prevent memory exhaustion when working on huge files (NTDS databases can grow to several gigabytes).
