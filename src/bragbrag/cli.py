"""CLI interface for the net worth tracker.

Starts the uvicorn backend web aplication on port 8000

"""

import uvicorn


def main():  # pragma: no cover
    """
    The main function executes on commands:
    This is your program's entry point.

    You can change this function to do whatever you want.
    Examples:
        * Run a test suite
        * Run a server
        * Do some other stuff
        * Run a command line application (Click, Typer, ArgParse)
        * List all available tasks
        * Run an application (Flask, FastAPI, Django, etc.)
    """

    from base import app
    uvicorn.run(app, host="0.0.0.0", port=8000)
