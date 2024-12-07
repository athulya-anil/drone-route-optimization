import logging

# Configure the logger
logging.basicConfig(
    filename="application.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,  # Change to DEBUG for verbose logging
)

# Get the logger instance
def get_logger(name):
    logger = logging.getLogger(name)
    return logger
