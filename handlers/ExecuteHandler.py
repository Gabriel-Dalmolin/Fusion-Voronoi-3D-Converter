import adsk.core 
import adsk.fusion

from ..scripts import convert_to_voronoi

class ExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, root):
        super().__init__()

        self.root = root


    def notify(self, args: adsk.core.CommandEventArgs) -> None:
        command = args.command
        inputs = command.commandInputs
        
        selection = adsk.core.SelectionCommandInput.cast(inputs.itemById("body")).selection(0)
        body = adsk.fusion.BRepBody.cast(selection.entity)

        radius = float(adsk.core.ValueCommandInput.cast(inputs.itemById("radius")).value)

        size = float(adsk.core.IntegerSpinnerCommandInput.cast(inputs.itemById("size")).value)

        lloyd = bool(adsk.core.BoolValueCommandInput.cast(inputs.itemById("lloyd")).value)
        
        convert_to_voronoi(self.root, body, radius, size, lloyd)
