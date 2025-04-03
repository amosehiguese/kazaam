import sys
import json
import logging
import typing import Dict, Any

from datetime import datetime
from logging.handlers import RotatingFileHandler

class StructuredFormatter(logging.Formatter):
    """Log formatter that outputs structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, "context"):
            log_data.update(record.context)

        return json.dumps(log_data)

    def setup_logging(log_level: str = "INFO", log_file: str = "oil_exploration.log") -> None:
        """Configure logging for production use."""
        logger = logging.getLogger()
        logger.setLevel(log_level)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(StructuredFormatter())
        logging.addHandler(console_handler)

        # File handler with rotattion
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024, #10MB
            backupCount=5,
        )

        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)

        # Configure third-party lib
        logging.getLogger("uvicorn").setLevel("WARNING")
        logging.getLogger("fastapi").setLevel("WARNING")

