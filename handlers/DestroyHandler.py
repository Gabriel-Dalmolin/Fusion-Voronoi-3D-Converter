import adsk.core
import adsk.fusion

class DestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self, baseFeature: adsk.fusion.BaseFeature):
        self.baseFeature = baseFeature
        super().__init__()

    def notify(self, eventArgs: adsk.core.CommandEventArgs) -> None:
        self.baseFeature.finishEdit()
        adsk.terminate()