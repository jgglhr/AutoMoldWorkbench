"""
AutoMoldWorkbench - Geometry Core
=================================

FunÃƒÂ§ÃƒÂµes bÃƒÂ¡sicas para anÃƒÂ¡lise de geometria no FreeCAD.

Este mÃƒÂ³dulo nÃƒÂ£o cria moldes.
Sua responsabilidade inicial ÃƒÂ© analisar uma geometria
existente e fornecer informaÃƒÂ§ÃƒÂµes normalizadas para os
mÃƒÂ³dulos posteriores do AutoMoldWorkbench.
"""

import FreeCAD

from automold.logger import logger


class GeometryError(Exception):
    """Erro relacionado ÃƒÂ  anÃƒÂ¡lise geomÃƒÂ©trica."""


class GeometryAnalyzer:
    """
    Analisa objetos geomÃƒÂ©tricos do FreeCAD.

    O objeto analisado deve possuir uma propriedade
    Shape vÃƒÂ¡lida.
    """

    def __init__(self, obj):
        self.obj = obj

        if obj is None:
            raise GeometryError("Objeto FreeCAD nÃƒÂ£o informado.")

        if not hasattr(obj, "Shape"):
            raise GeometryError(
                "O objeto informado nÃƒÂ£o possui uma propriedade Shape."
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
        Verifica se a geometria ÃƒÂ© vÃƒÂ¡lida.

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
        Verifica se a geometria contÃƒÂ©m pelo menos um sÃƒÂ³lido.

        Retorna:
            bool
        """

        try:
            return len(self.shape.Solids) > 0
        except Exception as exc:
            logger.error(
                "Erro ao verificar sÃƒÂ³lidos: %s",
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
        Retorna as dimensÃƒÂµes X, Y e Z da geometria.

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
    def face_count(self):
        """
        Retorna a quantidade de faces da geometria.

        Retorna:
            int
        """

        try:
            return len(self.shape.Faces)

        except Exception as exc:
            logger.error(
                "Erro ao contar faces: %s",
                exc
            )

            return 0

    def edge_count(self):
        """
        Retorna a quantidade de arestas da geometria.

        Retorna:
            int
        """

        try:
            return len(self.shape.Edges)

        except Exception as exc:
            logger.error(
                "Erro ao contar arestas: %s",
                exc
            )

            return 0

    def vertex_count(self):
        """
        Retorna a quantidade de vÃƒÂ©rtices da geometria.

        Retorna:
            int
        """

        try:
            return len(self.shape.Vertexes)

        except Exception as exc:
            logger.error(
                "Erro ao contar vÃƒÂ©rtices: %s",
                exc
            )

            return 0

    def surface_area(self):
        """
        Retorna a ÃƒÂ¡rea superficial total da geometria.

        Retorna:
            float
        """

        try:
            return self.shape.Area

        except Exception as exc:
            logger.error(
                "Erro ao obter ÃƒÂ¡rea superficial: %s",
                exc
            )

            raise GeometryError(
                "NÃƒÂ£o foi possÃƒÂ­vel obter a ÃƒÂ¡rea superficial."
            ) from exc

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
                "NÃƒÂ£o foi possÃƒÂ­vel obter o volume."
            ) from exc

    def center(self):
        """
        Retorna o centro geomÃƒÂ©trico da Bounding Box.

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
    def face_surfaces(self):
        """
        Analisa as superfÃƒÂ­cies de todas as faces.

        Retorna:
            list[dict]
        """

        surfaces = []

        for index, face in enumerate(
            self.shape.Faces,
            start=1
        ):
            try:
                surface = face.Surface
                surface_type = surface.__class__.__name__

                center = face.CenterOfMass

                surfaces.append({
                    "index": index,
                    "type": surface_type,
                    "area": face.Area,
                    "center": {
                        "x": center.x,
                        "y": center.y,
                        "z": center.z,
                    },
                })

            except Exception as exc:
                logger.error(
                    "Erro ao analisar face %s: %s",
                    index,
                    exc
                )

                surfaces.append({
                    "index": index,
                    "type": "Unknown",
                    "area": 0.0,
                    "center": {
                        "x": 0.0,
                        "y": 0.0,
                        "z": 0.0,
                    },
                })

        return surfaces

    def surface_types(self):
        """
        Retorna a quantidade de faces por tipo de superfÃƒÂ­cie.

        Exemplo:

            {
                "Plane": 6,
                "Cylinder": 2
            }

        Retorna:
            dict
        """

        result = {}

        for surface in self.face_surfaces():
            surface_type = surface["type"]

            result[surface_type] = (
                result.get(surface_type, 0) + 1
            )

        return result

    def face_normals(self):
        """
        Retorna a normal geomÃƒÂ©trica de cada face.

        Retorna:
            list[dict]
        """

        normals = []

        for index, face in enumerate(
            self.shape.Faces,
            start=1
        ):
            try:
                u_min, u_max, v_min, v_max = face.ParameterRange

                u = (u_min + u_max) / 2.0
                v = (v_min + v_max) / 2.0

                normal = face.normalAt(u, v)

                normals.append({
                    "index": index,
                    "normal": {
                        "x": normal.x,
                        "y": normal.y,
                        "z": normal.z,
                    },
                })

            except Exception as exc:
                logger.error(
                    "Erro ao obter normal da face %s: %s",
                    index,
                    exc
                )

                normals.append({
                    "index": index,
                    "normal": None,
                })

        return normals

    def orientation_analysis(self):
        """
        Classifica a orientaÃƒÂ§ÃƒÂ£o predominante de cada face.

        Retorna:
            list[dict]
        """

        orientations = []

        for item in self.face_normals():

            index = item["index"]
            normal = item["normal"]

            if normal is None:
                orientations.append({
                    "index": index,
                    "orientation": "UNKNOWN",
                })
                continue

            x = normal["x"]
            y = normal["y"]
            z = normal["z"]

            values = {
                "X_NEGATIVE": -x,
                "X_POSITIVE": x,
                "Y_NEGATIVE": -y,
                "Y_POSITIVE": y,
                "Z_NEGATIVE": -z,
                "Z_POSITIVE": z,
            }

            orientation = max(
                values,
                key=values.get
            )

            orientations.append({
                "index": index,
                "orientation": orientation,
                "normal": normal,
            })

        return orientations

    def summary(self):
        """
        Retorna um resumo completo da geometria analisada.

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

            "volume": self.volume(),

            "center": self.center(),

            "faces": self.face_count(),

            "edges": self.edge_count(),

            "vertices": self.vertex_count(),

            "surface_area": self.surface_area(),

            "dimensions": self.dimensions(),

            "surface_types": self.surface_types(),

            "surfaces": self.face_surfaces(),

            "normals": self.face_normals(),

            "orientations": self.orientation_analysis(),
        }


def analyze_object(obj):
    """
    FunÃƒÂ§ÃƒÂ£o auxiliar para analisar diretamente
    um objeto FreeCAD.

    Retorna:
        dict
    """

    analyzer = GeometryAnalyzer(obj)

    return analyzer.summary()
