# Maya libraries
import maya.cmds as mc
import maya.api.OpenMaya as om


def _getMFn(apiNode):
    kType = apiNode.apiType()
    MFn = lambda *args, **kwargs: None

    if apiNode.hasFn(kType):
        apiTypeStr = ''
        for i in dir(om.MFn):
            if kType == om.MFn.__getattribute__(om.MFn, i):
                apiTypeStr = i

        fnName = 'MFn'+apiTypeStr[1:]
        if fnName in dir(om):
            MFn = om.__dict__[fnName]

    return MFn(apiNode)


def getMObject(shapes):
    """Return the corresponding MObject(s) of the given shape(s).

    :param shapes: Node(s) name.
    :type shapes: str or list

    :returns: Corresponding MObject(s) of the given shape(s)
        The return type depends on the shapes parameter type.
    :rtype: str or list
    """
    isList = not isinstance(shapes, basestring)
    shapes = shapes if isList else [shapes]

    nodes = []
    for shape in shapes:
        mSl = om.MSelectionList()
        mSl.add(shape)
        nodes.append(mSl.getDependNode(0))

    return nodes if isList else nodes[0]


def getDagPath(shapes):
    isList = not isinstance(shapes, basestring)
    shapes = shapes if isList else [shapes]

    nodes = []
    for shape in shapes:
        mSl = om.MSelectionList()
        mSl.add(shape)
        nodes.append(mSl.getDagPath(0))

    return nodes if isList else nodes[0]


def getMDagPathMFn(nodes):
    isList = not isinstance(nodes, basestring)
    nodes = nodes if isList else [nodes]

    apiNodes = [getDagPath(node) for node in nodes]
    MFns = [_getMFn(apiNode) for apiNode in apiNodes]

    return (apiNodes, MFns) if isList else (apiNodes[0], MFns[0])


def getMObjMFn(nodes):
    isList = not isinstance(nodes, basestring)
    nodes = nodes if isList else [nodes]

    apiNodes = [getMObject(node) for node in nodes]
    MFns = [_getMFn(apiNode) for apiNode in apiNodes]

    return (apiNodes, MFns) if isList else (apiNodes[0], MFns[0])


def getMFn(nodes):
    _, MFns = getMObjMFn(nodes)
    return MFns
