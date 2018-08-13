# Maya libraries
import maya.cmds as mc


def clearKeys(nodes, ignores=[]):
    """Clear the animation keys on the given node(s).

    Arguments:
        nodes {str or list} -- Node(s) to remove the animations keys from.

    Keyword Arguments:
        ignores {str or list} -- (default: {[]})
            Attribute(s) to ignore during the cut key process.
    """
    nodes = [nodes] if isinstance(nodes, basestring) else nodes
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    for node in nodes:
        lnSnAttrs = zip(mc.listAttr(node, k=1), mc.listAttr(node, k=1, sn=1))
        for lnAttr, snAttr in lnSnAttrs:
            if not ((lnAttr in ignores) or (snAttr in ignores)):
                mc.cutKey(node, at=lnAttr)


def connectChannelBox(source, destinations, ignores=[]):
    """Connect the shared keyable attributes from the source to the destination(s).

    Arguments:
        source {str} -- Object who will be the source of the connection(s).
        destinations {str or list} -- Object(s) who will be the destination of the
            connection(s).

    Keyword Arguments:
        ignores {str or list} -- (default: {[]})
            Attribute(s) to ignore during the connection process.
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

    Arguments:
        nodes {str or list} -- Node(s) to disconnect the attribute(s) from.

    Keyword Arguments:
        ignores {str or list} -- (default: {[]})
            Attribute(s) to ignore during the disconnection process.
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

    Arguments:
        nodes {str or list} -- Node(s) to lock the keyable attribute(s) on.

    Keyword Arguments:
        ignores {list} -- (default: {[]})
            Attribute(s) to ignore during the lock process.
    """
    nodes = [nodes] if isinstance(nodes, basestring) else nodes
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    for node in nodes:
        lnSnAttrs = zip(mc.listAttr(node, k=1), mc.listAttr(node, k=1, sn=1))
        for lnAttr, snAttr in lnSnAttrs:
            if not ((lnAttr in ignores) or (snAttr in ignores)):
                mc.setAttr(node+'.'+lnAttr.split('.')[0], lock=True)


def unlockChannelBox(nodes, ignores=[]):
    """Unlock the keyable attribute(s) on the given node(s).

    Arguments:
        nodes {str or list} -- Node(s) to unlock the keyable attribute(s) on.

    Keyword Arguments:
        ignores {list} -- (default: {[]})
            Attribute(s) to ignore during the unlock process.
    """
    nodes = [nodes] if isinstance(nodes, basestring) else nodes
    ignores = [ignores] if isinstance(ignores, basestring) else ignores

    for node in nodes:
        lnSnAttrs = zip(mc.listAttr(node, k=1), mc.listAttr(node, k=1, sn=1))
        for lnAttr, snAttr in lnSnAttrs:
            if not ((lnAttr in ignores) or (snAttr in ignores)):
                mc.setAttr(node+'.'+lnAttr.split('.')[0], lock=False)
