import adsk.core
import adsk.fusion

def gen_mirrored_ghost_points(
        seeds: list[list[int]],
        bBox: adsk.core.BoundingBox3D
) -> list[list[int]]:  
    new_seeds = []
    
    for seed in seeds:
        min_p = bBox.minPoint
        max_p = bBox.maxPoint

        x = seed[0]
        y = seed[1]
        z = seed[2]

        n_x_offset = (x - min_p.x) # Negative and positive offsets to mirror 
        p_x_offset = (max_p.x - x)
        n_y_offset = (y - min_p.y)  
        p_y_offset = (max_p.y - y)
        n_z_offset = (z - min_p.z)  
        p_z_offset = (max_p.z - z)

        new_seeds.append([(min_p.x - n_x_offset), y, z])
        new_seeds.append([(max_p.x + p_x_offset), y, z])
        new_seeds.append([x, (min_p.y - n_y_offset), z])
        new_seeds.append([x, (max_p.y + p_y_offset), z])
        new_seeds.append([x, y, (min_p.z - n_z_offset)])
        new_seeds.append([x, y, (max_p.z + p_z_offset)])

    return new_seeds