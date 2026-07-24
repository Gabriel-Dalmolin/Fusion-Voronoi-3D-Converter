import traceback

import adsk.core
import adsk.fusion

from .sweep_edge import sweep_edge
from .revolve_vertex import revolve_vertex

revolved_points = []

def sweep_voronoi_edges(root: adsk.fusion.Component, bodies, edges: list[list[adsk.core.Point3D]], radius) -> adsk.fusion.BRepBody:
    bodies = adsk.core.ObjectCollection.create()

    for e in edges:
        p1 = e[0]
        p2 = e[1]

        sketch = root.sketches.add(root.xYConstructionPlane)
        curve = sketch.sketchCurves.sketchLines.addByTwoPoints(p1, p2)

        sweep_edge(root, radius, curve, p1, bodies)

        sketch.deleteMe()

        if p1 not in revolved_points:
            revolved_points.append(p1)
        if p2 not in revolved_points:
            revolved_points.append(p2)

    for p in revolved_points:
        revolve_vertex(root, radius, p, bodies)

    combines = root.features.combineFeatures
    b1 = adsk.fusion.BRepBody.cast(bodies.item(0))
    bodies.removeByIndex(0)
    combineInput = combines.createInput(b1, bodies) 
    combineInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation # type: ignore
    combines.add(combineInput)

    return b1