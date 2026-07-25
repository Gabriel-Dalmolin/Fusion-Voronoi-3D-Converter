import traceback

import scipy
import scipy.spatial

import adsk.core
import adsk.fusion

from .math.gen_mirrored_ghost_points import gen_mirrored_ghost_points
from .math.get_random_seeds import get_random_seeds
from .math.gen_ghost_points import gen_ghost_points
from .math.get_voronoi_edges import get_voronoi_edges
from .fusionManipulation.combine_bodies import combine_bodies
from .fusionManipulation.intersect_bodies import intersect_bodies
from .fusionManipulation.create_wireframe import create_wireframe
from .fusionManipulation.sweep_voronoi_edges import sweep_voronoi_edges
from .fusionManipulation.create_face_connections import create_face_connections

def convert_to_voronoi(root: adsk.fusion.Component, body: adsk.fusion.BRepBody, radius, n_seeds):
    try: 
        bodies = adsk.core.ObjectCollection.create()
        seeds = []

        wireframe_bodies, vertices = create_wireframe(root, body, radius)
        for b in wireframe_bodies:
            bodies.add(b)

        seeds += get_random_seeds(body, n_seeds)

        ghost_index = len(seeds)

        bBox = body.boundingBox
        seeds += gen_mirrored_ghost_points(seeds, bBox)
        # seeds += gen_ghost_points(body)

        # for s in seeds:   # Used for visualizing the seeds
        #     vertex = adsk.core.Point3D.create(s[0], s[1], s[2])
        #     revolve_vertex(root, radius, vertex, bodies)

        voronoi = scipy.spatial.Voronoi(seeds + vertices)

        interceptions, edges = get_voronoi_edges(body, voronoi, ghost_index)
        adsk.core.Application.get().log(str(len(interceptions)))
        # create_face_connections(root, bodies, interceptions, radius)
        v_edges = sweep_voronoi_edges(root, bodies, edges, radius)

        obj_collection = adsk.core.ObjectCollection.create()
        obj_collection.add(v_edges)
        for b in bodies:
            obj_collection.add(b)

        target = adsk.fusion.BRepBody.cast(obj_collection.item(0))

        combine_bodies(root, obj_collection)

        intersect_bodies(root, target, body)

    except:
        adsk.core.Application.get().log(traceback.format_exc())
