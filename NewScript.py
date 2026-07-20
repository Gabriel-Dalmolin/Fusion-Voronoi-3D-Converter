"""This file acts as the main module for this script."""

from re import A
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

def createBox():
    plane = root.xYConstructionPlane
    sketch = root.sketches.add(plane)

    lines = sketch.sketchCurves.sketchLines

    p1 = adsk.core.Point3D.create(0,0,0)
    p2 = adsk.core.Point3D.create(5,5,0)

    lines.addTwoPointRectangle(p1, p2)

    profile = sketch.profiles.item(0)

    extrudes = root.features.extrudeFeatures
    distance = adsk.core.ValueInput.createByReal(2)

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

class ExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args: adsk.core.CommandEventArgs) -> None:
        command = args.command
        inputs = command.commandInputs

        widthInput = adsk.core.ValueCommandInput.cast(inputs.itemById("width"))
        width = widthInput.value

class UICommand(adsk.core.CommandCreatedEventHandler):
    def notify(self, args: adsk.core.CommandCreatedEventArgs) -> None:
        command = args.command

        inputs = command.commandInputs

        inputs.addValueInput(
            "width",
            "Width",
            "mm",
            adsk.core.ValueInput.createByString("50 mm")
        )

        executeHandler = ExecuteHandler()
        command.execute.add(executeHandler)
        handlers.append(executeHandler)


def get_input():
    cmdDef = ui.commandDefinitions.addButtonDefinition(
        "MyCommand",
        "My Command",
        "Creates my command"
    )

    handler = UICommand()
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
