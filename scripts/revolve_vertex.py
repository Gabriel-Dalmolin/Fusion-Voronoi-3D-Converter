import adsk.core
import adsk.fusion

import math

def revolve_vertex(
        root: adsk.fusion.Component, 
        radius, 
        vertex: adsk.core.Point3D, 
        bodies: adsk.core.ObjectCollection):

    x = vertex.x
    y = vertex.y
    z = vertex.z

    planes = root.constructionPlanes
    planeInput = root.constructionPlanes.createInput()

    offset = adsk.core.ValueInput.createByReal(z)
    planeInput.setByOffset(root.xYConstructionPlane, offset)

    plane = planes.add(planeInput)

    sketch = root.sketches.add(plane)
    lines = sketch.sketchCurves.sketchLines
    arcs = sketch.sketchCurves.sketchArcs

    p1 = sketch.modelToSketchSpace(adsk.core.Point3D.create(x + radius,y,z))
    p2 = sketch.modelToSketchSpace(adsk.core.Point3D.create(x - radius,y,z)) 

    axis = lines.addByTwoPoints(p1, p2)
    arcs.addByCenterStartEnd(sketch.modelToSketchSpace(vertex), p1, p2)

    profile = sketch.profiles.item(0)
    
    revolves = root.features.revolveFeatures
    revolveInput = revolves.createInput(
        profile,
        axis, 
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation #type: ignore
    )

    revolveAngle = adsk.core.ValueInput.createByReal(math.pi)
    revolveInput.setAngleExtent(True, revolveAngle)
    
    b = revolves.add(revolveInput).bodies
    for i in b:
        bodies.add(i)

    plane.deleteMe()
    sketch.deleteMe()