#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from thrift_app.thrift_server import run_thrift_server


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapps2024.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if os.environ.get('RUN_MAIN', None) != 'true':
        from thrift_app.thrift_server import run_thrift_server
        run_thrift_server()
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
