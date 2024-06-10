#   _____             _    __  __              _
#  |  __ \           | |  |  \/  |            | |
#  | |__) |___   ___ | |_ | \  / |  __ _  ___ | |_  ___  _ __
#  |  ___// _ \ / __|| __|| |\/| | / _` |/ __|| __|/ _ \| '__|
#  | |   | (_) |\__ \| |_ | |  | || (_| |\__ \| |_|  __/| |
#  |_|    \___/ |___/ \__||_|  |_| \__,_||___/ \__|\___||_|
#
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'post_master.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
