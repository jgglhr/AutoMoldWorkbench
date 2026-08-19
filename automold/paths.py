"""
AutoMold filesystem paths.
"""

from pathlib import Path


PACKAGE_ROOT = Path("automold")

PROJECT_ROOT = Path(".")

RESOURCES_DIR = PROJECT_ROOT / "resources"

ICONS_DIR = RESOURCES_DIR / "icons"

UI_DIR = RESOURCES_DIR / "ui"

DOCS_DIR = PROJECT_ROOT / "docs"

EXAMPLES_DIR = PROJECT_ROOT / "examples"

TESTS_DIR = PROJECT_ROOT / "tests"