"""This file acts as the main module for this script."""

import traceback

import adsk.core
import adsk.fusion

from .handlers import CommandHandler
from .utils import download_requirements

import sys

app = adsk.core.Application.get()
ui  = app.userInterface
design = adsk.fusion.Design.cast(app.activeProduct)

handlers = []

if not design:
    print("No Fusion design is active.")
else:
    root = design.rootComponent

def create_voronoi():
    baseFeature = root.features.baseFeatures.add()
    baseFeature.startEdit()

    cmdDef = ui.commandDefinitions.itemById("Voronoi_converter")
    if not cmdDef:
        cmdDef = ui.commandDefinitions.addButtonDefinition(
            "Voronoi_converter",
            "Voronoi Converter",
            "Convert a body to a 3D voronoi structure"
        )

    handler = CommandHandler(handlers, root, baseFeature)
    cmdDef.commandCreated.add(handler)
    handlers.append(handler)

    cmdDef.execute()

def main():
    app.log(u'TextCommandWindow.Clear')
    download_requirements()
    adsk.autoTerminate(False)

    create_voronoi()

def run(_context: str):
    try:
        main()
    except:  #pylint:disable=bare-except
        app.log(f'Failed:\n{traceback.format_exc()}')