"""This file acts as the main module for this script."""

import traceback

import adsk.core
import adsk.fusion
# import adsk.cam
# import adsk.drawing

# Initialize the global variables for the Application and UserInterface objects.
app = adsk.core.Application.get()
ui  = app.userInterface
design = adsk.fusion.Design.cast(app.activeProduct)

handlers = []

if not design:
    print("No Fusion design is active.")
else:
    root = design.rootComponent

def createBox(x, y, z):
    plane = root.xYConstructionPlane
    sketch = root.sketches.add(plane)

    lines = sketch.sketchCurves.sketchLines

    p1 = adsk.core.Point3D.create(0,0,0)
    p2 = adsk.core.Point3D.create(x,y,0)

    lines.addTwoPointRectangle(p1, p2)

    profile = sketch.profiles.item(0)

    extrudes = root.features.extrudeFeatures
    distance = adsk.core.ValueInput.createByReal(z)

    extrudeInput = extrudes.createInput(
        profile,
        adsk.fusion.FeatureOperations.NewBodyFeatureOperation # type: ignore
    )

    distanceDef = adsk.fusion.DistanceExtentDefinition.create(distance)
    extrudeInput.setOneSideExtent(
        distanceDef,
        adsk.fusion.ExtentDirections.PositiveExtentDirection # type: ignore
    )

    extrudes.add(extrudeInput)

class DestroyHandler(adsk.core.CommandEventHandler):
    def notify(self, eventArgs: adsk.core.CommandEventArgs) -> None:
        adsk.terminate()

class ExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args: adsk.core.CommandEventArgs) -> None:
        command = args.command
        inputs = command.commandInputs

        x = int(adsk.core.ValueCommandInput.cast(inputs.itemById("x")).value)
        y = int(adsk.core.ValueCommandInput.cast(inputs.itemById("y")).value)
        z = int(adsk.core.ValueCommandInput.cast(inputs.itemById("z")).value)
        
        createBox(x,y,z)

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args: adsk.core.CommandCreatedEventArgs) -> None:
        command = args.command

        inputs = command.commandInputs

        inputs.addValueInput(
            "x",
            "Size in X (mm)",
            "mm",
            adsk.core.ValueInput.createByString("50 mm")
        )
        inputs.addValueInput(
            "y",
            "Size in Y (mm)",
            "mm",
            adsk.core.ValueInput.createByString("50 mm")
        )
        inputs.addValueInput(
            "z",
            "Size in Z (mm)",
            "mm",
            adsk.core.ValueInput.createByString("50 mm")
        )

        executeHandler = ExecuteHandler()
        command.execute.add(executeHandler)
        handlers.append(executeHandler)

        destroyHandler = DestroyHandler()
        command.destroy.add(destroyHandler)
        handlers.append(destroyHandler)


def get_input():
    cmdDef = ui.commandDefinitions.itemById("Voronoi_converter")
    if not cmdDef:
        cmdDef = ui.commandDefinitions.addButtonDefinition(
            "Voronoi_converter",
            "Voronoi Converter",
            "Convert a body to a 3D voronoi structure"
        )

    handler = CommandHandler()
    cmdDef.commandCreated.add(handler)
    handlers.append(handler)

    cmdDef.execute()

def main():
    adsk.autoTerminate(False)

    get_input()

def run(_context: str):
    """This function is called by Fusion when the script is run."""

    try:
        main()
    except:  #pylint:disable=bare-except
        # Write the error message to the TEXT COMMANDS window.
        app.log(f'Failed:\n{traceback.format_exc()}')
