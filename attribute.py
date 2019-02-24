# Maya libraries
import maya.cmds as mc
import pymel.core as pm
import maya.api.OpenMaya as om


def iterChannelbox(nodes, ignores=tuple()):
    """Yield channelbox attribute(s) of the given nodes.

    :param nodes: Maya's node(s) name in a list.
    :type nodes: list or tuple or set

    :param ignores: Node's attribute(s) name in a list to ignore during the process,
        defaults to tuple()
    :type ignores: list or tuple or set, optional

    :returns: Pymel's attribute object
    :rtype: {pymel.core.general.Attribute}
    """
    for node in nodes:
        node = pm.PyNode(node) if isinstance(node, basestring) else node

        for attr in node.listAttr():
            attr_is_keyable_and_unlocked = attr.isKeyable() and (not attr.isLocked())
            attr_is_in_channelbox = attr.isInChannelBox()

            if attr_is_keyable_and_unlocked or attr_is_in_channelbox:
                short_name_in_ignores = attr.shortName() in ignores
                long_name_in_ignores = attr.longName() in ignores

                if not (short_name_in_ignores or long_name_in_ignores):
                    yield attr


def defaultChannelbox(nodes, ignores=tuple()):
    """Set the values of the channelbox attributes to there default if there is.

    :param nodes: Maya's node(s) name in a list.
    :type nodes: list or tuple or set

    :param ignores: Node's attribute(s) name in a list to ignore during the process,
        defaults to tuple()
    :type ignores: list or tuple or set, optional
    """

    for attr in iterChannelbox(nodes, ignores):
        if attr.attrName() in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
            defaultValue = 0
        elif attr.attrName() in ('sx', 'sy', 'sz', 'v'):
            defaultValue = 1
        else:
            defaultValue = pm.addAttr(attr, query=True, defaultValue=True)

        if not (defaultValue is None):
            attr.set(defaultValue)


def connectChannelbox(source, destinations, ignores=tuple()):
    """Connect the source channelbox's attribute(s) to the destination(s)
    channelbox's attribute(s).

    :param source: Maya's node name.
        Connects to the given destination Maya's node(s).
    :type source: str or PyNode

    :param destinations: Maya's node name(s) in a list.
        Receive the connection from the given source Maya's node.
    :type destinations: [type]

    :param ignores: Node's attribute(s) name in a list to ignore during the process,
        defaults to tuple()
    :type ignores: list or tuple or set, optional
    """
    source = pm.PyNode(source)
    iterDestinations = (pm.PyNode(destination) for destination in destinations)

    for destinationAttr in iterChannelbox(iterDestinations, ignores):
        try:
            sourceAttr = source.attr(destinationAttr.shortName())
            sourceAttr >> destinationAttr
        except:
            wrngMsg = "Can't connect {0} to {1}."
            pm.warning(wrngMsg.format(sourceAttr.name(), destinationAttr.name()))


def disconnectChannelbox(nodes, ignores=tuple()):
    """Disconnect the keyable attributes of the given node(s).

    :param nodes: Node(s) to disconnect the attribute(s) from.
    :type nodes: str or list

    :param ignores: Defaults to []
        Attribute(s) to ignore during the disconnection process.
    :type ignores: str or list, optional
    """
    for destinationAttr in iterChannelbox(nodes, ignores):
        sourceAttr = destinationAttr.listConnections(source=True, plugs=True)
        sourceAttr = (sourceAttr or [None])[0]
        if sourceAttr:
             destinationAttr // sourceAttr


def lockChannelbox(nodes, ignores=[]):
    """Lock the keyable attribute(s) on the given node(s).

    :param nodes: Node(s) to lock the keyable attribute(s) on.
    :type nodes: str or list

    :param ignores: Defaults to []
        Attribute(s) to ignore during the lock process.
    :type ignores: str or list, optional
    """

    nodes = [nodes] if isinstance(nodes, basestring) else nodes
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    for node in nodes:
        lnSnAttrs = zip(
            mc.listAttr(node, k=1) or [None],
            mc.listAttr(node, k=1, sn=1) or [None])

        for lnAttr, snAttr in lnSnAttrs:

            if ((not lnAttr) or (not snAttr)):
                continue

            if not ((lnAttr in ignores) or (snAttr in ignores)):
                mc.setAttr(node+'.'+lnAttr.split('.')[0], lock=True)


def unlockChannelbox(nodes, ignores=[]):
    """Unlock the keyable attribute(s) on the given node(s).

    :param nodes: Node(s) to unlock the keyable attribute(s) on.
    :type nodes: str or list

    :param ignores: Defaults to []
        Attribute(s) to ignore during the unlock process.
    :type ignores: str or list, optional
    """

    nodes = [nodes] if isinstance(nodes, basestring) else nodes
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    for node in nodes:
        lnSnAttrs = zip(
            mc.listAttr(node, k=1) or [None],
            mc.listAttr(node, k=1, sn=1) or [None])

        for lnAttr, snAttr in lnSnAttrs:

            if ((not lnAttr) or (not snAttr)):
                continue

            if not ((lnAttr in ignores) or (snAttr in ignores)):
                mc.setAttr(node+'.'+lnAttr.split('.')[0], lock=False)


def clearKeys(nodes, ignores=[]):
    """Clear the animation keys on the given node(s).

    :param nodes: Node(s) to remove the animations keys from.
    :type nodes: str or list

    :param ignores: Defaults to []
        Attribute(s) to ignore during the cut key process.
    :type ignores: str or list, optional
    """

    nodes = [nodes] if isinstance(nodes, basestring) else nodes
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    for node in nodes:
        lnSnAttrs = zip(mc.listAttr(node, k=1) or [], mc.listAttr(node, k=1, sn=1))
        for lnAttr, snAttr in lnSnAttrs:
            if not ((lnAttr in ignores) or (snAttr in ignores)):
                mc.cutKey(node, at=lnAttr)

