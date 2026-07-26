import adsk.core
import adsk.fusion

def gen_mirrored_ghost_points(
        seeds: list[list[int]],
        body: adsk.fusion.BRepBody
) -> list[list[int]]:  
    bBox = body.boundingBox
    app = adsk.core.Application.get()

    measureMgr = app.measureManager
    
    new_seeds = []

    for seed in seeds:
        for face in body.faces:
            point = adsk.core.Point3D.create(
                seed[0],
                seed[1],
                seed[2]
            )

            result = measureMgr.measureMinimumDistance(face, point)
            min_dist_point = result.positionTwo

            new_seeds.append(
                [
                    2 * min_dist_point.x - point.x,
                    2 * min_dist_point.y - point.y,
                    2 * min_dist_point.z - point.z,
                ]
            )

    return new_seeds