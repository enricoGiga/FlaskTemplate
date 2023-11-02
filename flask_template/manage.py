"""
Utility manager for common commands
"""


import subprocess
import sys
import unittest

import coverage
from flask.cli import FlaskGroup

from app import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)


# code coverage
COV = coverage.coverage(
    branch=True,
    include="server/*",
    omit=[
        "tests/*",
    ],
)
COV.start()




@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover("tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary:")
        COV.report()
        COV.html_report()
        COV.erase()
        sys.exit(0)
    else:
        sys.exit(1)


@cli.command()
def flake():
    """Runs flake8 on the server folder."""
    subprocess.run(["flake8", "server"], shell=True, check=False)


if __name__ == "__main__":
    cli()
