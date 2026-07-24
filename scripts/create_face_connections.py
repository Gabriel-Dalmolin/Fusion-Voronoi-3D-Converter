import adsk.core
import adsk.fusion

from .revolve_vertex import revolve_vertex
from .sweep_edge import sweep_edge
import random

def create_face_connections(
        root: adsk.fusion.Component, 
        bodies, 
        interceptions: list[tuple[adsk.fusion.BRepFace, list[adsk.core.Point3D]]], 
        radius):
    for i in interceptions:
        face = i[0]
        points = i[1]

        for p1 in points:
            edges = face.edges
            n_edges = len(edges)
            edge = edges.item(random.randint(0, n_edges-1))

            success, start, end = edge.evaluator.getParameterExtents()
            success_, p2 = edge.evaluator.getPointAtParameter(random.uniform(start, end))

            sketch = root.sketches.add(root.xYConstructionPlane)
            lines = sketch.sketchCurves.sketchLines
            line = lines.addByTwoPoints(p1, p2)

            sweep_edge(root, radius, line, p1, bodies)

            sketch.deleteMe()
