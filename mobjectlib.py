# Maya libraries
import maya.cmds as mc
import maya.api.OpenMaya as om


def getMObject(nodes):
    """Return the corresponding MObject(s) of the given node(s).

    Arguments:
        nodes {str or list} -- Node(s) name.

    Returns:
        str or list -- Corresponding MObject(s) of the given node(s)
            The return type depends on the nodes parameter type.
    """
    isList = True
    if isinstance(nodes, basestring):
        nodes, isList = [nodes], False

    mObjs = []
    for node in nodes:
        selectionList = om.MSelectionList()
        selectionList.add(node)
        mObjs.append(selectionList.getDependNode(0))

    return mObjs if isList else mObjs[0]
