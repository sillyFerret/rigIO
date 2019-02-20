# Python libraries
import json

# Maya libraries
import maya.cmds as mc
import maya.OpenMaya as om


class Selection(object):
    """ Simple class to manage selection in Maya.
    """

    def __init__(self):
        self._selection = self.selection
        self.mode = "replace"

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return self.__class__.__name__+' : '+str(self.selection)

    @property
    def selection(self):
        """Return the current Maya selection.

        :returns: Current Maya selection.
        :rtype: list
        """
        return mc.ls(sl=True, fl=True, l=True)

    @selection.setter
    def selection(self, selection):
        """Set the current selection with the given object(s) list.

        :param selection: Object to select.
        :type selection: list
        """
        self._selection = selection
        mc.select(self._selection, **{self.mode: 1})

    def _viewSelection(func):
        """Decorator to automatically add a return to the class function and
        print in the script editor the result of the selection.

        All the function under the Selection class should return and print the
        current selection after the computation of a given method.

        :param func: Method in the Selection class.
        :type func: function

        :returns: The given method within the Selection class with a return and
            a print statement.
        :rtype: function
        """

        def wrapper(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.view()
            return self.selection

        return wrapper

    def view(self):
        """Print in the Maya's script editor the current selection.
        """
        selectionString = "Result: "
        readableSelection = [i.split('|')[-1] for i in self.selection]
        selectionString += json.dumps(readableSelection, indent=4)
        om.MGlobal.displayInfo(selectionString)

    @_viewSelection
    def reverseOrder(self):
        """Reverse the order of your current selection.
        """
        self.mode = "replace"
        self.selection = self.selection[::-1]

    @_viewSelection
    def sort(self, mode="name"):
        """Sort the current selection according to the given mode.

        :param mode: defaults to "name"
            Can be set to 'name'.
            name : Will sort your current selection by alphabetical order.
        :type mode: str, optional
        """
        if str(mode).lower() == "name":
            self.selection = sorted(self.selection)

    @_viewSelection
    def hierarchy(self):
        """Select the all the decedent of your current selection.
        """
        self.mode = "replace"
        self.selection += \
            (mc.listRelatives(self.selection, ad=1, f=1) or [])[::-1]

    @_viewSelection
    def typeUnder(self, objectType, mode="replace"):
        """Select all the descendant matching the given objectType under your
        current selection.

        :param objectType: [description]
        :type objectType: [type]

        :param mode: [description], defaults to "replace"
        :type mode: str, optional
        """
        self.mode = mode
        allDescendent = (
            self.selection +
            (mc.listRelatives(self.selection, ad=1, f=1) or [])[::-1])
        self.selection = mc.ls(allDescendent, type=objectType) or []

    @_viewSelection
    def mirror(self, mode="replace"):
        """[summary]

        [description]
        :param mode: [description], defaults to "replace"
        :type mode: str, optional
        """
        self.mode = mode
        sides = ['l_', 'r_']
        mirrObj = []
        for obj in self.selection:
            objN = obj.split('|')[-1]
            nms = ':'.join(objN.split(':')[:-1])
            objN = objN.split(':')[-1]
            currSide = objN[:2]
            for i, side in enumerate(sides):
                if currSide == side:
                    objN = objN.replace(objN[:len(side)], sides[1-i])
                    objN = ':'.join([nms, objN]) if nms else objN
                    mirrObj.append(objN)

        self.selection = mc.ls(mirrObj)
