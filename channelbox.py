import pymel.core as pm

import pymel.core as pm


class ChannelBox(list):
    """
    Manage channelBox attributes.
    """

    def __init__(self, node, ignores=tuple()):
        """
        :param node: Maya's node name.
        :type node: str or PyNode

        :param ignores: Attribute(s) name to ignore during the process,
            defaults to tuple()
        :type ignores: list(str) or tuple(str) or set(str), optional

        :Example: x = channelBox('nodeName', ignores=['visibility'])
        """
        self.node = pm.PyNode(node) if isinstance(node, basestring) else node
        self.ignores = ignores

        super(ChannelBox, self).__init__(self.__iter__())

    def __repr__(self):
        className = self.__class__.__name__
        foundAttr = super(ChannelBox, self).__repr__()
        return '%s : %s' % (className, foundAttr)

    def __iter__(self):
        for attr in self.node.listAttr():

            if attr.isKeyable() or attr.isInChannelBox():
                short_name_in_ignores = attr.shortName() in self.ignores
                long_name_in_ignores = attr.longName() in self.ignores

                if not (short_name_in_ignores or long_name_in_ignores):
                    yield attr

    def __getitem__(self, index):

        if isinstance(index, int):
            return super(ChannelBox, self).__getitem__(index)

        elif isinstance(index, pm.general.Attribute):
            for attr in self:
                if index.shortName() == attr.shortName():
                    return attr
            raise KeyError(index)

        elif isinstance(index, (str, unicode)):
            for attr in self:
                if index in (attr.longName(), attr.shortName()):
                    return attr
            raise KeyError(index)

        else:
            errorMessage = '%s indices must be integers ' % self.__class__.__name__
            errorMessage += 'str or pymel.core.general.Attribute. '
            errorMessage += 'Gets %s' % type(index)
            raise TypeError(errorMessage)

    def __contains__(self, key):
        if not isinstance(key, pm.general.Attribute):
            return super(ChannelBox, self).__contains__(key)
        else:
            for attr in self:
                if key.longName() == attr.longName():
                    return True
        return False

    def get(self, key, default=None):
        """[summary]

        [description]
        :param key: [description]
        :type key: [type]
        :param default: [description], defaults to None
        :type default: [type], optional
        :returns: [description]
        :rtype: {[type]}
        """
        return self[key] if key in self else default

    def setDefault(self):
        """
        Set the values of the channelBox attributes to there default if there is.
        """
        for attr in self:
            if attr.attrName() in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
                defaultValue = 0
            elif attr.attrName() in ('sx', 'sy', 'sz', 'v'):
                defaultValue = 1
            else:
                defaultValue = pm.addAttr(attr, query=True, defaultValue=True)

            if not (defaultValue is None):
                try:
                    attr.set(defaultValue)
                except RuntimeError as message:
                    pm.warning(message.message[:-1])

    def connect(self, *args):
        """
        Connect the source channelBox's attribute(s) to the destination(s)
        channelBox's attribute(s).

        :param args: Maya's node channelBoxAttribute object in a list.
        :type args: ChannelBox Class's instance
        """
        for channelBox in args:

            if not isinstance(channelBox, ChannelBox):
                channelBox = ChannelBox(channelBox)

            for attr in channelBox:
                sourceAttr = self.get(attr)
                if sourceAttr:
                    try:
                        sourceAttr >> attr
                    except RuntimeError as error:
                        pm.warning(error.message[:-1])

    def disconnect(self):
        """
        Disconnect the keyable attributes of the given node(s).
        """
        for attr in self:
            sourceAttr = attr.listConnections(source=True, plugs=True)
            sourceAttr = (sourceAttr or [None])[0]

            if sourceAttr and sourceAttr.isSource():
                sourceAttr // attr
            else:
                message = '%s has no incoming connections.' % attr.name()
                pm.warning(message)

    def setLocked(self, value):
        """Lock the keyable attribute(s) on the given node(s).

        :param nodes: Node(s) to lock the keyable attribute(s) on.
        :type nodes: str or list

        :param ignores: Defaults to []
            Attribute(s) to ignore during the lock process.
        :type ignores: str or list, optional
        """
        for attr in self:
            attr.setLocked(value)
