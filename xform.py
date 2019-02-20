import pymel.core as pm


def match(target, destinations, t=True, r=True, s=True):
    """Match the world space transformation(s) of the given objects.

    :param target: Source object.
    :type target: str

    :param destinations: [description]
    :type destinations: [type]

    :param t: defaults to True
    :type t: bool, optional

    :param r: defaults to True
    :type r: bool, optional

    :param s: [description], defaults to True
    :type s: bool, optional
    """
    if isinstance(destinations, basestring):
        destinations = [destinations]

    target = pm.PyNode(target)
    destinations = pm.PyNode(destinations)

    # Get the target object matrix.
    targetMatrix = target.worldMatrix.get()

    # Apply the target matrix to the given destinations objects.
    for destination in destinations:
        destinationMatrix = destination.parentInverseMatrix.get() * targetMatrix

        if all((t,r,x)):
            destination.setTransformation(destinationMatrix)
        else:
            if t: destination.setTranslation(destinationMatrix.translate)
            if r: destination.setRotation(destinationMatrix.rotate)
            if s: destination.setScale(destinationMatrix.scale)


def clearLocal(transforms, t=True, r=True, s=True):
    """Clear the local transformation(s) of the given transform object(s).

    :param transforms: [description]
    :type transforms: str or list

    :param t: defaults to True
        If True, will clear the translations XYZ of the given object(s).
        Else the translations will be ignore during the clear process.
    :type t: bool, optional

    :param r: defaults to True
        If True, will clear the rotations XYZ of the given object(s).
        Else the rotations will be ignore during the clear process.
    :type r: bool, optional

    :param s: defaults to True
        If True, will clear the scales XYZ of the given object(s).
        Else the scales will be ignore during the clear process.
    :type s: bool, optional
    """
    if isinstance(transforms, basestring):
        transforms = [transforms]

    transforms = pm.PyNode(transforms)

    for transform in transforms:
        for axis in 'xyz':
            if t:
                try:
                    transform.attr('t'+axis).set(0)
                except:
                    pass
            if r:
                try:
                    transform.attr('r'+axis).set(0)
                except:
                    pass
            if s:
                try:
                    transform.attr('s'+axis).set(1)
                except:
                    pass
