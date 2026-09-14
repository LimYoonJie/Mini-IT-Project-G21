"""Django entry point kept under the original app.py filename."""
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecommerce.settings")


def main():
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
