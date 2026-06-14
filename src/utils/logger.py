import logging

from src.config.settings import LOG_DIR, LOG_FILE


def get_logger():

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
    )

    return logging.getLogger(
        "customer_support_assistant"
    )