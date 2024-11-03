import pathlib
import json
import logging.config
import logging.handlers


logger = logging.getLogger("bragbrag")


def settup_logging():
    """Settup logging from a json config file."""
    config_file = pathlib.Path("logging_configs/config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)


def example_add(a, b):
    """Add two values to test the intial project setup.

    Example function that can be tested using pytest. Used to test if
    the automated testing is correctly configured at the project
    intialization.

    Parameters
    ----------
    a : int
        first input
    b : int
        second input

    Examples
    --------
    FIXME: Add docs.

    """
    add_response = a + b
    logger.debug(f"The add response is {add_response}.")
    return (add_response)


def main():
    settup_logging()
    print(example_add(10, 2))


if __name__ == "__main__":
    main()
