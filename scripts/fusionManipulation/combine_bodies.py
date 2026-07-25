import adsk.fusion
import adsk.core

def combine_bodies(root, bodies: adsk.core.ObjectCollection):
    combines = root.features.combineFeatures
    b1 = adsk.fusion.BRepBody.cast(bodies.item(0))
    bodies.removeByIndex(0)
    combineInput = combines.createInput(b1, bodies) 
    combineInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation # type: ignore
    combines.add(combineInput)

    return b1