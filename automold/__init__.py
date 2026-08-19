"""
AutoMold Workbench
==================

FreeCAD GUI initialization.
"""

import FreeCADGui


class AutoMoldWorkbench(FreeCADGui.Workbench):
    """Main AutoMold FreeCAD Workbench."""

    MenuText = "AutoMold"

    ToolTip = "Automatic mold generation Workbench"

    def Initialize(self):
        """Initialize menus, commands and toolbars."""

        self.appendMenu(
            "AutoMold",
            [],
        )

    def Activated(self):
        """Called when AutoMold becomes the active Workbench."""

        pass

    def Deactivated(self):
        """Called when AutoMold is deactivated."""

        pass

    def GetClassName(self):
        """Return the FreeCAD Python Workbench class name."""

        return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(AutoMoldWorkbench())
