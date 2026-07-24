import random

import adsk.core
import adsk.fusion

def get_random_seeds(body: adsk.fusion.BRepBody, n):
    seeds = []
    c = 0

    bbox = body.boundingBox
    min_p = bbox.minPoint
    max_p = bbox.maxPoint

    while c < n:
        point = adsk.core.Point3D.create(
            random.uniform(min_p.x, max_p.x),
            random.uniform(min_p.y, max_p.y),
            random.uniform(min_p.z, max_p.z),
        )

        if body.pointContainment(point) == adsk.fusion.PointContainment.PointInsidePointContainment:
            c += 1
            seeds.append(point.asArray()) 

    return seeds
