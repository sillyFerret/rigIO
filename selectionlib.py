# Python libraries
import json

# Maya libraries
import maya.cmds as mc
import maya.OpenMaya as om


class Selection(object):
    """Simple class to handle the selection in maya.
    """

    def __init__(self, selection=None, mode="replace"):
        self._selection = selection or self.selection
        self.mode = mode

    @property
    def selection(self):
        return mc.ls(selection=True, flatten=True)

    @selection.setter
    def selection(self, selection):
        self._selection = selection
        mc.select(self._selection, **{self.mode: True})

    def _viewSelection(func):
        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.view()
            return self.selection
        return wrapper

    def view(self):
        selectionString = "Result: "
        selectionString += json.dumps(self.selection, indent=4)
        om.MGlobal.displayInfo(selectionString)

    @_viewSelection
    def reverseOrder(self, mode="replace"):
        self.mode = mode
        self.selection = self.selection[::-1]

    @_viewSelection
    def sort(self, mode="name"):
        if mode.lower() == "name":
            self.selection = sorted(self.selection)

    @_viewSelection
    def hierarchy(self, mode="replace"):
        self.mode = mode
        self.selection += \
            mc.listRelatives(self.selection, allDescendents=True) or []

    def mirror(self, mode="replace"):
        pass
