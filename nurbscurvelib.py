# Maya libraries
import maya.cmds as mc
import maya.api.OpenMaya as om

# Custom libraries
from customlib import mobjectlib


def getUParam(curve, transforms, percentage=False):
    """Returns the closest UParameter of the given transform(s) on a given curve.

    Arguments:
        curve {str} -- Curve to get the UParameter from.
        transforms {str or list} -- Transforms to get the closest UParameter.

    Keyword Arguments:
        percentage {bool} -- (default: {False})
            If True, will return the UParameter in a percentage ratio.
            If False, will return the UParameter in it's parametric form.

    Returns:
        int or list -- The closest UParameter.
    """
    # Param checkers
    isList = True
    if isinstance(transforms, basestring):
        transforms, isList = [transforms], False

    # Get the curveShape
    crvShp = mc.listRelatives(curve, s=1, ni=1)[0]

    # Get the mayaApi MCurve object and function sets from the curveShape name.
    mCurve = mobjectlib.getMObject(crvShp)
    fnCurve = om.MFnNurbsCurve(mCurve)

    uParams = []
    for transform in transforms:
        pnt = mc.xform(transform, q=1, ws=1, t=1)
        mPnt = om.MPoint(*pnt)
        _, uParam = fnCurve.closestPoint(mPnt)

        if percentage:
            uParam = fnCurve.findLengthFromParam(uParam)
            uParam = uParam / fnCurve.length()

        uParams.append(uParam)

    # If the given parameter isn't a list,
    # I expect the function to return a single value.
    return uParams if isList else uParams[0]


def _pointOnCurve(curve, transforms):
    """[summary]

    [description]

    Arguments:
        curve {str} -- [description]
        transforms {str or list} -- [description]

    Returns:
        str or list -- [description]
    """
    isList = True
    if isinstance(transforms, basestring):
        transforms, isList = [transforms], False

    pocis = []
    crvShp = mc.listRelatives(curve, s=1, ni=1)[0]
    for transform in transforms:
        # Get and create the needed stuff
        uParam = getUParam(curve, transform)
        poci = transform.replace(transform.split('_')[-1], 'poci')
        poci = mc.createNode('pointOnCurveInfo', n=poci)
        # Connect the stuff together
        mc.connectAttr(crvShp+'.worldSpace[0]', poci+'.inputCurve', f=1)
        mc.setAttr(poci+'.parameter', uParam)
        mc.connectAttr(poci+'.position', transform+'.translate', f=1)

        pocis.append(poci)

    return pocis if isList else pocis[0]


def _motionPath(curve, transforms):
    """[summary]

    [description]

    Arguments:
        curve {str} -- [description]
        transforms {str or list} -- [description]

    Returns:
        str or list -- [description]
    """
    isList = True
    if isinstance(transforms, basestring):
        transforms, isList = [transforms], False

    mps = []
    crvShp = mc.listRelatives(curve, s=1, ni=1)[0]
    for transform in transforms:
        # Get and create the needed stuff
        uParam = getUParam(curve=curve, transforms=transform, percentage=True)
        mp = transform.replace(transform.split('_')[-1], 'mp')
        mp = mc.createNode('motionPath', n=mp)
        # Connect the stuff together
        mc.connectAttr(crvShp+'.worldSpace[0]', mp+'.geometryPath', f=1)
        mc.setAttr(mp+'.uValue', uParam)
        mc.setAttr(mp+'.fractionMode', True)
        mc.connectAttr(mp+'.allCoordinates', transform+'.translate', f=1)
        mc.connectAttr(mp+'.rotate', transform+'.rotate', f=1)
        mc.connectAttr(mp+'.rotateOrder', transform+'.rotateOrder', f=1)

        mps.append(mp)

    return mps if isList else mps[0]


def attachToCurve(curve, transforms, mode='pointOnCurve'):
    """[summary]

    [description]

    Arguments:
        curve {str} -- [description]
        transforms {str or list} -- [description]

    Keyword Arguments:
        mode {str} -- [description] (default: {'pointOnCurve'})

    Returns:
        str or list -- [description]
    """

    if mode.lower() == 'pointoncurve':
        return _pointOnCurve(curve, transforms)

    elif mode.lower() == 'motionpath':
        return _motionPath(curve, transforms)


def getShapeData(curves):
    """[summary]

    [description]

    Arguments:
        curves {string or list} -- [description]

    Returns:
        dict -- [description]
    """
    curves = [curves] if isinstance(curves, basestring) else curves
    crvsDict = {}
    for curve in curves:
        crvDict = crvsDict.setdefault(curve, {})
        crvShps = mc.listRelatives(curve, s=True, ni=True)

        for i, crvShp in enumerate(crvShps):
            shpDict = crvDict.setdefault(i, {})
            shpDict['degree'] = mc.getAttr(crvShp+'.degree')
            shpDict['form'] = mc.getAttr(crvShp+'.form')
            cvs = shpDict.setdefault('point', [])

            for cv in mc.ls(crvShp+'.cv[*]', fl=True):
                cvs.append(mc.xform(cv, q=1, t=1))

    return crvsDict
