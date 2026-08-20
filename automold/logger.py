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
    # Internal formatting
    # --------------------------------------------------------------

    def _format_message(self, message, args):
        """Format a logging message using the standard % style."""

        if not args:
            return str(message)

        try:
            return str(message) % args
        except (TypeError, ValueError):
            return " ".join(
                [str(message)] + [str(arg) for arg in args]
            )

    # --------------------------------------------------------------
    # Internal output
    # --------------------------------------------------------------

    def _write_console(self, level, message, *args):
        """Write a message to the Python console."""

        if level not in self.LEVELS:
            level = "INFO"

        if self.LEVELS[level] < self.LEVELS[self.level]:
            return

        message = self._format_message(message, args)

        timestamp = datetime.datetime.now().strftime(
            "%H:%M:%S"
        )

        print(
            "[AutoMold] "
            "[" + timestamp + "] "
            "[" + level + "] "
            + message
        )

    # --------------------------------------------------------------
    # Logging methods
    # --------------------------------------------------------------

    def debug(self, message, *args):
        """Log a debug message."""

        self._write_console(
            "DEBUG",
            message,
            *args,
        )

    def info(self, message, *args):
        """Log an informational message."""

        self._write_console(
            "INFO",
            message,
            *args,
        )

    def warning(self, message, *args):
        """Log a warning message."""

        self._write_console(
            "WARNING",
            message,
            *args,
        )

    def error(self, message, *args):
        """Log an error message."""

        self._write_console(
            "ERROR",
            message,
            *args,
        )

    def critical(self, message, *args):
        """Log a critical message."""

        self._write_console(
            "CRITICAL",
            message,
            *args,
        )


# Global logger instance

logger = AutoMoldLogger()
