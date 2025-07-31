import logging
import sys

def setup_logging():
    """
    Sets up a centralized logger for the entire application.

    This function configures the root logger to output timestamped messages
    to standard output. It should be called once when the application starts.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout,
    )
    logging.info("Logging has been configured centrally.")