"""
AutoMold Workbench - Exceptions
================================

Custom exception hierarchy used by AutoMold.

The purpose of these exceptions is to allow each module to report
specific and understandable errors instead of using generic
Exception objects.
"""


class AutoMoldError(Exception):
    """
    Base exception for all AutoMold errors.
    """

    def __init__(self, message):
        self.message = str(message)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class AutoMoldConfigurationError(AutoMoldError):
    """
    Error related to AutoMold configuration.
    """

    pass


class AutoMoldMeshError(AutoMoldError):
    """
    Error related to mesh/STL processing.
    """

    pass


class AutoMoldGeometryError(AutoMoldError):
    """
    Error related to FreeCAD geometry operations.
    """

    pass


class AutoMoldMoldError(AutoMoldError):
    """
    Error related to mold generation.
    """

    pass


class AutoMoldBooleanError(AutoMoldGeometryError):
    """
    Error during boolean operations.

    Examples:
        - Cut
        - Fuse
        - Common
        - Split
    """

    pass


class AutoMoldExportError(AutoMoldError):
    """
    Error while exporting generated files.
    """

    pass


class AutoMoldImportError(AutoMoldError):
    """
    Error while importing external files.
    """

    pass


class AutoMoldValidationError(AutoMoldError):
    """
    Error when input data fails validation.
    """

    pass


class AutoMoldCancelledError(AutoMoldError):
    """
    Operation was intentionally cancelled by the user.
    """

    pass