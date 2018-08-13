# Maya libraries
import maya.cmds as mc


def hasUnfrozenVertex(shape):
    """Checks if the given shape has unfrozen vertices.

    For each vertex, the function gets XYZ transformations, if it finds a value,
    it breaks the for loop and return True.

    Arguments:
        shape {string} -- Name of the shape you want to check the vertices.

    Returns:
        bool -- True if the given shape has unfrozen vertices.
            False if the given shape doesn't have unfrozen vertices.
    """
    # Get the data out of the shape.
    polyData = mc.polyEvaluate(shape)

    # If the given shape isn't a polygonal object,
    # polyEvaluate returns a string.
    if isinstance(polyData, basestring):
        return

    # Loop into the vertices of the given object.
    if polyData.has_key('vertex'):
        for vtx in set(range(polyData['vertex'])):
            for axis in 'xyz':
                if mc.getAttr('{}.pnts[{}].pnt{}'.format(shape, vtx, axis)):
                    return True
        return False


def isIntermiate(shape):
    """Checks if the given shape is an intermediate object.

    Gets the value of the shapes intermediateObject attribute if it has one.

    Arguments:
        shape {string} -- Name of the shape you want to check the intermediate object
            status.
    """
    return (mc.objExists('{}.intermediateObject'.format(shape)) and
            mc.getAttr('{}.intermediateObject'.format(shape)))
