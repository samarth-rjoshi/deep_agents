import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name: str = "deep_research") -> logging.Logger:
    """
    Sets up a logger that writes to both console and a log file.
    The log file is located at <project_root>/logs/backend.log.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding handlers multiple times if logger is already configured
    if logger.hasHandlers():
        return logger

    # Determine project root (assuming this file is in backend/src/deep_research/utils/)
    # We need to go up 4 levels: utils -> deep_research -> src -> backend -> PROJECT_ROOT
    current_file = Path(__file__).resolve()
    project_root = current_file.parents[4]
    
    # Ensure logs directory exists
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    log_file = logs_dir / "backend.log"

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # File Handler
    file_handler = RotatingFileHandler(
        log_file, maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create a default logger instance
logger = setup_logger()
