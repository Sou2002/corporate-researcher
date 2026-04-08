"""Centralized logger for use across all modules.

Usage:
    from logger import get_logger
    logger = get_logger(__name__)

    logger.debug("Detailed debug info")
    logger.info("Process started")
    logger.warning("Something unexpected")
    logger.error("Something failed: %s", err)
    logger.critical("Fatal error")
"""

import logging
import sys
from pathlib import Path


def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Return a named logger with console and optional file handlers.

    Args:
        name:  Pass __name__ from the calling module.
        level: Minimum log level (default: DEBUG).

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if the logger is already configured.
    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Console handler (stdout) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_file_logger(
    name: str,
    log_file: str = "app.log",
    level: int = logging.DEBUG,
    file_level: int = logging.WARNING,
) -> logging.Logger:
    """Return a logger that writes to both console and a log file.

    Args:
        name:       Pass __name__ from the calling module.
        log_file:   Path to the log file (created if it doesn't exist).
        level:      Minimum level for console output (default: DEBUG).
        file_level: Minimum level written to file (default: WARNING).

    Returns:
        Configured Logger instance.
    """
    logger = get_logger(name, level)

    # Skip adding file handler if one already exists.
    if any(isinstance(h, logging.FileHandler) for h in logger.handlers):
        return logger

    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger