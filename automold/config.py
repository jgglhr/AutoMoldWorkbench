"""
AutoMoldWorkbench - Configuration Manager

Gerencia as configurações persistentes do AutoMold
através do sistema ParameterGrp do FreeCAD.
"""

import FreeCAD


class AutoMoldConfig:
    """Gerenciador das configurações do AutoMold."""

    # Caminho das configurações no FreeCAD
    PARAMETER_PATH = "User parameter:BaseApp/Preferences/Mod/AutoMold"

    # Valores padrão
    DEFAULT_MOLD_CLEARANCE = 0.3
    DEFAULT_PIN_CLEARANCE = 0.2
    DEFAULT_PIN_DIAMETER = 6.0
    DEFAULT_SHRINKAGE = 0.0

    DEFAULT_LANGUAGE = "auto"
    DEFAULT_LOG_LEVEL = "INFO"

    DEFAULT_AUTO_REPAIR = True

    def __init__(self):
        """Inicializa o acesso ao grupo de parâmetros do FreeCAD."""

        self.params = FreeCAD.ParamGet(self.PARAMETER_PATH)

    def initialize_defaults(self):
        """
        Cria parâmetros que ainda não existem.

        Parâmetros existentes NÃO são sobrescritos.
        """

        existing = {
            name
            for param_type, name, value in self.params.GetContents()
        }

        if "Language" not in existing:
            self.params.SetString(
                "Language",
                self.DEFAULT_LANGUAGE
            )

        if "LogLevel" not in existing:
            self.params.SetString(
                "LogLevel",
                self.DEFAULT_LOG_LEVEL
            )

        if "MoldClearance" not in existing:
            self.params.SetFloat(
                "MoldClearance",
                self.DEFAULT_MOLD_CLEARANCE
            )

        if "Shrinkage" not in existing:
            self.params.SetFloat(
                "Shrinkage",
                self.DEFAULT_SHRINKAGE
            )

        if "PinDiameter" not in existing:
            self.params.SetFloat(
                "PinDiameter",
                self.DEFAULT_PIN_DIAMETER
            )

        if "PinClearance" not in existing:
            self.params.SetFloat(
                "PinClearance",
                self.DEFAULT_PIN_CLEARANCE
            )

        if "AutoRepair" not in existing:
            self.params.SetBool(
                "AutoRepair",
                self.DEFAULT_AUTO_REPAIR
            )

        if "Initialized" not in existing:
            self.params.SetBool(
                "Initialized",
                True
            )

    # ---------------------------------------------------------
    # GETTERS
    # ---------------------------------------------------------

    def get_float(self, name, default=0.0):
        """Obtém um parâmetro float."""

        return self.params.GetFloat(name, default)

    def get_int(self, name, default=0):
        """Obtém um parâmetro inteiro."""

        return self.params.GetInt(name, default)

    def get_string(self, name, default=""):
        """Obtém um parâmetro string."""

        return self.params.GetString(name, default)

    def get_bool(self, name, default=False):
        """Obtém um parâmetro booleano."""

        return self.params.GetBool(name, default)

    # ---------------------------------------------------------
    # SETTERS
    # ---------------------------------------------------------

    def set_float(self, name, value):
        """Salva um parâmetro float."""

        self.params.SetFloat(name, float(value))

    def set_int(self, name, value):
        """Salva um parâmetro inteiro."""

        self.params.SetInt(name, int(value))

    def set_string(self, name, value):
        """Salva um parâmetro string."""

        self.params.SetString(name, str(value))

    def set_bool(self, name, value):
        """Salva um parâmetro booleano."""

        self.params.SetBool(name, bool(value))

    # ---------------------------------------------------------
    # RESET
    # ---------------------------------------------------------

    def reset(self):
        """
        Remove todas as configurações do AutoMold
        e recria os valores padrão.
        """

        self.params.Clear()
        self.initialize_defaults()


# Instância global utilizada pelo Workbench
config = AutoMoldConfig()