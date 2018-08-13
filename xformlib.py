# Maya libraries
import maya.cmds as mc


def match(source, destinations, t=True, r=True, s=True):
    """Match the world space transformation of the destination object(s) to the
    source object.

    Arguments:
        source {str} -- Source object.
        destinations {str or list} -- Object(s) to match the source xform.

    Keyword Arguments:
        t {bool} -- (default: {True})
            If true, will match the position of the destinations objects to the
            source object base on it's pivot point location.
        r {bool} -- (default: {True})
            If true, will match the rotation of the destinations objects to the
            source object.
        s {bool} -- (default: {True})
            If true, will match the scale of the destinations objects to the source
            object.
    """
    if isinstance(destinations, basestring):
        destinations = [destinations]

    # Get the source object xform data.
    t = mc.xform(source, q=True, piv=True, ws=True)[:3] if t else t
    r = mc.xform(source, q=True, ro=True, ws=True) if r else r
    s = mc.xform(source, q=True, s=True, ws=True) if s else s

    # Apply the source xform data to the given destinations objects
    for dest in destinations:
        if t:
            mc.xform(dest, t=t, ws=True)
        if r:
            mc.xform(dest, ro=r, ws=True)
        if s:
            mc.xform(dest, s=s, ws=True)
