"""
AutoMold Workbench - Logger
===========================

Simple logging system for AutoMold.

The logger uses Python print() for console output so it works
reliably inside the FreeCAD Python Console.
"""

import datetime


class AutoMoldLogger:
    """Simple logger for AutoMold Workbench."""

    LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }

    def __init__(self):
        """Create the logger."""

        self.level = "INFO"

    # --------------------------------------------------------------
    # Configuration
    # --------------------------------------------------------------

    def set_level(self, level):
        """Set the minimum logging level."""

        level = str(level).upper()

        if level not in self.LEVELS:
            raise ValueError(
                "Invalid log level: " + level
            )

        self.level = level

    # --------------------------------------------------------------
    # Internal output
    # --------------------------------------------------------------

    def _write_console(self, level, message):
        """Write a message to the Python console."""

        if level not in self.LEVELS:
            level = "INFO"

        if self.LEVELS[level] < self.LEVELS[self.level]:
            return

        timestamp = datetime.datetime.now().strftime(
            "%H:%M:%S"
        )

        print(
            "[AutoMold] "
            "[" + timestamp + "] "
            "[" + level + "] "
            + str(message)
        )

    # --------------------------------------------------------------
    # Logging methods
    # --------------------------------------------------------------

    def debug(self, message):
        """Log a debug message."""

        self._write_console(
            "DEBUG",
            message,
        )

    def info(self, message):
        """Log an informational message."""

        self._write_console(
            "INFO",
            message,
        )

    def warning(self, message):
        """Log a warning message."""

        self._write_console(
            "WARNING",
            message,
        )

    def error(self, message):
        """Log an error message."""

        self._write_console(
            "ERROR",
            message,
        )

    def critical(self, message):
        """Log a critical message."""

        self._write_console(
            "CRITICAL",
            message,
        )


# Global logger instance

logger = AutoMoldLogger()