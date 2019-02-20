# Maya libraries
import maya.cmds as mc
import pymel.core as pm
import maya.api.OpenMaya as om


def getInChannelbox(node):
    """Returns the attribute(s) in the channelbox for the given node.

    Iterate into the attribute list of the given node and return only the
    attribute(s) and return only the attribute who are either keyable and not locked
    OR channelboxed.

    :param node: Node name or a PyNode node.
    :type node: str or PyNode

    :returns: Attribute(s) in the channelbox
    :rtype: list(pymel.core.general.Attribute)
    """
    node = pm.PyNode(node) if isinstance(node, basestring) else node

    inChannelbox = []
    for attr in node.listAttr():

        attr_is_keyable_and_unlocked = attr.isKeyable() and (not attr.isLocked())
        attr_is_in_channelbox = attr.isInChannelBox()

        if attr_is_keyable_and_unlocked or attr_is_in_channelbox:
            inChannelbox.append(attr)

    return inChannelbox


def defaultChannelBox(nodes, ignores=tuple()):
    """[summary]

    [description]
    :param nodes: [description]
    :type nodes: [type]
    :param ignores: [description], defaults to []
    :type ignores: list, optional
    """

    def channelbox_attribute_iterator(nodes, ignores):
        for node in nodes:
            for attr in getInChannelbox(node):
                short_name_in_ignores = attr.shortName() in ignores
                long_name_in_ignores = attr.longName() in ignores
                if not (short_name_in_ignores or long_name_in_ignores):
                    yield attr

    for attr in channelbox_attribute_iterator(nodes, ignores):
        if attr.attrName() in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
            defaultValue = 0
        elif attr.attrName() in ('sx', 'sy', 'sz', 'v'):
            defaultValue = 1
        else:
            defaultValue = pm.addAttr(attr, query=True, defaultValue=True)

        if not (defaultValue is None):
            attr.set(defaultValue)


def connectChannelBox(source, destinations, ignores=[]):

    destinations = [destinations] if isinstance(destinations, basestring) else destinations
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    source = pm.PyNode(source)
    destinations = pm.PyNode(destinations)
    connectionDict = {}

    for destination in destinations:
        for attr in getInChannelbox(destination):

            short_name_in_ignores = (attr.shortName() in ignores)
            long_name_in_ignores = (attr.longName() in ignores)

            if not (short_name_in_ignores or long_name_in_ignores):
                sourceAttr = source.attr(attr.shortName())
                toConnect = connectionDict.setdefault(sourceAttr, [])
                toConnect.append(attr)

    for sourceAttr, destinationAttrs in connectionDict.items():
        for destinationAttr in destinationAttrs:
            try:
                sourceAttr >> destinationAttr
            except:
                wrngMsg = 'Can\'t connect {0} to {1}.'
                pm.warning(wrngMsg.format(destinationAttr.name(), sourceAttr.name()))


def connectChannelBox_OLD(source, destinations, ignores=[]):
    """Connect the shared keyable attributes from the source to the destination(s).

    :param source: Object who will be the source of the connection(s).
    :type source: str

    :param destinations: Object(s) who will be the destination of the connection(s).
    :type destinations: str or list

    :param ignores: Defaults to []
        Attribute(s) to ignore during the connection process.
    :type ignores: str or list, optional
    """

    if isinstance(destinations, basestring):
        destinations = [destinations]
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    lnSnAttrs = zip(mc.listAttr(source, k=1), mc.listAttr(source, k=1, sn=1))
    for destination in destinations:
        for lnAttr, snAttr in lnSnAttrs:
            if not ((lnAttr in ignores) or (snAttr in ignores)):
                try:
                    mc.connectAttr(source+'.'+lnAttr, destination+'.'+lnAttr)
                except:
                    wrngMsg = 'Can\'t connect {1}.{0} to {2}.{0}.'
                    mc.warning(wrngMsg.format(lnAttr, source, destination))


def disconnectChannelBox(nodes, ignores=[]):
    """Disconnect the keyable attributes of the given node(s).

    :param nodes: Node(s) to disconnect the attribute(s) from.
    :type nodes: str or list

    :param ignores: Defaults to []
        Attribute(s) to ignore during the disconnection process.
    :type ignores: str or list, optional
    """

    nodes = [nodes] if isinstance(nodes, basestring) else nodes
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    for node in nodes:
        lnSnAttrs = zip(mc.listAttr(node, k=1), mc.listAttr(node, k=1, sn=1))
        for lnAttr, snAttr in lnSnAttrs:
            if not ((lnAttr in ignores) or (snAttr in ignores)):
                conn = mc.listConnections(node+'.'+lnAttr, d=0, s=1, p=1)
                conn = (conn or [None])[0]
                if conn:
                    mc.disconnectAttr(conn, node+'.'+lnAttr)


def lockChannelBox(nodes, ignores=[]):
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


def unlockChannelBox(nodes, ignores=[]):
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

