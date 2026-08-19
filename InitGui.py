"""
AutoMold Workbench
==================
"""

import FreeCADGui


class AutoMoldWorkbench(FreeCADGui.Workbench):

    MenuText = "AutoMold"

    ToolTip = "Automatic mold generation Workbench"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):

        from automold.logger import logger

        logger.info(
            "AutoMold Workbench inicializado"
        )

    def Activated(self):

        from automold.logger import logger

        logger.info(
            "AutoMold Workbench ativado"
        )

    def Deactivated(self):

        from automold.logger import logger

        logger.info(
            "AutoMold Workbench desativado"
        )


FreeCADGui.addWorkbench(
    AutoMoldWorkbench()
)