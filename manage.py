#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import dotenv
import os
import sys


def main():
    """Run administrative tasks."""
    dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'StayEz_Backend.settings')
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






# import os
# import sys

# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings_dev')  # Default to development settings
#     if 'runserver' in sys.argv:
#         os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings_dev')  # Use development settings for runserver command
#     else:
#         os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings_prod')  # Use production settings for other commands

#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)

# if __name__ == '__main__':
#     main()
