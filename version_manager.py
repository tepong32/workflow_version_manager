"""Portable entry point for Version Manager.

Copy this file together with the ``version_manager`` package into any Git
repository, then run ``python version_manager.py --help``.
"""

from version_manager.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
