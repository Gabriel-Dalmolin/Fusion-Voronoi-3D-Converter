import adsk.core
import adsk.fusion

from .ExecuteHandler import ExecuteHandler
from .DestroyHandler import DestroyHandler

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, handlers, root, baseFeature: adsk.fusion.BaseFeature):
        super().__init__()

        self.handlers = handlers
        self.root = root
        self.baseFeature = baseFeature

    def notify(self, args: adsk.core.CommandCreatedEventArgs) -> None:
        command = args.command

        inputs = command.commandInputs

        bodyInput = inputs.addSelectionInput(
            "body",
            "Body",
            "Select the body you want to convert"
        )

        bodyInput.addSelectionFilter("Bodies")

        inputs.addValueInput(
            "radius",
            "Radius of connections (mm)",
            "mm",
            adsk.core.ValueInput.createByString("1 mm")
        )

        inputs.addIntegerSpinnerCommandInput(
            "seeds",
            "Number of seeds",
            0,
            1000,
            1, 
            5
        )

        executeHandler = ExecuteHandler(self.root)
        command.execute.add(executeHandler)
        self.handlers.append(executeHandler)

        destroyHandler = DestroyHandler(self.baseFeature)
        command.destroy.add(destroyHandler)
        self.handlers.append(destroyHandler)