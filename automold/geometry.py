"""
AutoMoldWorkbench - Geometry Core
=================================

Funções básicas para análise de geometria no FreeCAD.

Este módulo não cria moldes.
Sua responsabilidade inicial é analisar uma geometria
existente e fornecer informações normalizadas para os
módulos posteriores do AutoMoldWorkbench.
"""

import FreeCAD

from automold.logger import logger


class GeometryError(Exception):
    """Erro relacionado à análise geométrica."""


class GeometryAnalyzer:
    """
    Analisa objetos geométricos do FreeCAD.

    O objeto analisado deve possuir uma propriedade
    Shape válida.
    """

    def __init__(self, obj):
        self.obj = obj

        if obj is None:
            raise GeometryError("Objeto FreeCAD não informado.")

        if not hasattr(obj, "Shape"):
            raise GeometryError(
                "O objeto informado não possui uma propriedade Shape."
            )

        if obj.Shape.isNull():
            raise GeometryError(
                "O objeto possui uma geometria nula."
            )

        self.shape = obj.Shape

        logger.debug(
            "GeometryAnalyzer criado para: %s",
            getattr(obj, "Name", "<sem nome>")
        )

    def is_valid(self):
        """
        Verifica se a geometria é válida.

        Retorna:
            bool
        """

        try:
            return self.shape.isValid()
        except Exception as exc:
            logger.error(
                "Erro ao validar geometria: %s",
                exc
            )
            return False

    def is_solid(self):
        """
        Verifica se a geometria contém pelo menos um sólido.

        Retorna:
            bool
        """

        try:
            return len(self.shape.Solids) > 0
        except Exception as exc:
            logger.error(
                "Erro ao verificar sólidos: %s",
                exc
            )
            return False

    def bounding_box(self):
        """
        Retorna a Bounding Box da geometria.

        Retorna:
            FreeCAD.BoundBox
        """

        return self.shape.BoundBox

    def dimensions(self):
        """
        Retorna as dimensões X, Y e Z da geometria.

        Retorna:
            dict:
                {
                    "x": float,
                    "y": float,
                    "z": float
                }
        """

        box = self.bounding_box()

        return {
            "x": box.XLength,
            "y": box.YLength,
            "z": box.ZLength,
        }

    def volume(self):
        """
        Retorna o volume da geometria.

        Retorna:
            float
        """

        try:
            return self.shape.Volume
        except Exception as exc:
            logger.error(
                "Erro ao obter volume: %s",
                exc
            )
            raise GeometryError(
                "Não foi possível obter o volume."
            ) from exc

    def center(self):
        """
        Retorna o centro geométrico da Bounding Box.

        Retorna:
            dict:
                {
                    "x": float,
                    "y": float,
                    "z": float
                }
        """

        box = self.bounding_box()

        center = box.Center

        return {
            "x": center.x,
            "y": center.y,
            "z": center.z,
        }

    def summary(self):
        """
        Retorna um resumo da geometria analisada.

        Retorna:
            dict
        """

        return {
            "name": getattr(
                self.obj,
                "Name",
                None
            ),
            "label": getattr(
                self.obj,
                "Label",
                None
            ),
            "valid": self.is_valid(),
            "solid": self.is_solid(),
            "dimensions": self.dimensions(),
            "volume": self.volume(),
            "center": self.center(),
        }


def analyze_object(obj):
    """
    Função auxiliar para analisar diretamente
    um objeto FreeCAD.

    Retorna:
        dict
    """

    analyzer = GeometryAnalyzer(obj)

    return analyzer.summary()