import pymel.core as pm


# Functions #########################################################################

def setDefault(nodes, ignores=tuple()):
    """Set the node(s) channelBox attributes(s) to there default value if there is.
    Log a warning message if a RuntimeError occur during the set value process.

    :param nodes:
        OR Maya node(s) name.
        OR PyNode instance(s) of Maya node(s).
    :type nodes:
        OR iterable of basestring
        OR iterable of pymel.core.PyNode

    :param ignores: Attribute(s) name to ignore during the process,
        defaults to tuple()
    :type ignores: Iterable of basestring, optional

   :Example:
        import maya.cmds as mc
        import rigIO.channelBox

        rigIO.channelBox.setDefault(mc.ls(sl=True), ['v'])
    """
    for node in nodes:
        channelBox = ChannelBox(node, *ignores)
        channelBox.setDefault()

def connect(source, destinations, ignores=tuple()):
    """Connect current channelBox attribute(s) to the destination(s)
    channelBox attribute(s). Log a warning message if a RuntimeError occurs
    during the connection process.

    :param source:
        OR Maya node name.
        OR PyNode instance of Maya node.
    :type source:
        OR basestring
        OR pymel.core.PyNode

    :param destinations:
        OR Maya node(s) name.
        OR PyNode instance(s) of Maya node(s).
    :type destinations:
        OR iterable of basestring
        OR iterable of pymel.core.PyNode

    :param ignores: Attribute(s) name to ignore during the process,
        defaults to tuple()
    :type ignores: Iterable of basestring, optional

   :Example:
        import maya.cmds as mc
        import rigIO.channelBox

        sl = mc.ls(sl=True)
        rigIO.channelBox.connect(sl[0], sl[1:], ['v'])
    """
    sourceChannelBox = ChannelBox(source, *ignores)
    sourceChannelBox.connect(*destinations)

def disconnect(nodes, ignores=tuple()):
    """Disconnect the node(s) channelBox attribute(s).
    Log a warning error if there is no incoming connection(s).

    :param nodes:
        OR Maya node(s) name.
        OR PyNode instance(s) of Maya node(s).
    :type nodes:
        OR iterable of basestring
        OR iterable of pymel.core.PyNode

    :param ignores: Attribute(s) name to ignore during the process,
        defaults to tuple()
    :type ignores: Iterable of basestring, optional

   :Example:
        import maya.cmds as mc
        import rigIO.channelBox

        rigIO.channelBox.disconnect(mc.ls(sl=True), ['v'])
    """
    for node in nodes:
        channelBox = ChannelBox(node, *ignores)
        channelBox.disconnect()

def setLocked(nodes, value, ignores=tuple()):
    """Delete the animation key(s) on the node chennelBox attribute(s).

    :param nodes:
        OR Maya node(s) name.
        OR PyNode instance(s) of Maya node(s).
    :type nodes:
        OR iterable of basestring
        OR iterable of pymel.core.PyNode

    :param value:
        True  - Lock the channelBox attribute(s).
        False - Unlock the channelBox attribute(s).
    :type value: bool

    :param ignores: Attribute(s) name to ignore during the process,
        defaults to tuple()
    :type ignores: Iterable of basestring, optional

   :Example:
        import maya.cmds as mc
        import rigIO.channelBox

        rigIO.channelBox.setLocked(mc.ls(sl=True), True, ['v'])
    """
    for node in nodes:
        channelBox = ChannelBox(node, *ignores)
        channelBox.setLocked(value)

def clearKeys(nodes, ignores=tuple()):
    """Delete the animation key(s) on the node chennelBox attribute(s).

    :param nodes:
        OR Maya node(s) name.
        OR PyNode instance(s) of Maya node(s).
    :type nodes:
        OR iterable of basestring
        OR iterable of pymel.core.PyNode

    :param ignores: Attribute(s) name to ignore during the process,
        defaults to tuple()
    :type ignores: Iterable of basestring, optional

   :Example:
        import maya.cmds as mc
        import rigIO.channelBox

        rigIO.channelBox.clearKeys(mc.ls(sl=True), ['v'])
    """
    for node in nodes:
        channelBox = ChannelBox(node, *ignores)
        channelBox.clearKeys()

# Class #############################################################################

class ChannelBox(tuple):
    """
    Class to manage a node channelBox attributes.
    """
    def __new__(cls, node, *ignores):
        """__new__(node, *ignores) method of builtins.type instance
        Create and return a new object.

        :param node:
            OR Maya node name.
            OR PyNode instance.
        :type node:
            OR str
            OR pymel.core.PyNode

        :param *ignores: Attribute(s) name to ignore during the process.
        :type *ignores: str
        """
        cls.node = pm.PyNode(node) if isinstance(node, basestring) else node
        cls._ignores = ignores

        content = tuple()
        for attr in cls.node.listAttr():
            if attr.isKeyable() or attr.isInChannelBox():
                content += attr,

        return tuple.__new__(cls, content)

    def __repr__(self):
        """repr(x) <-> x.__repr__()
        """
        return repr(tuple(i.longName() for i in self._filter()))

    def __getitem__(self, index):
        """x.[0] <-> x.__getitem__(0)

        :param index:
            OR Index number of the wanted attribute.
            OR Name of the wanted attribute.
            OR Pymel attribute.
        :type index:
            OR int
            OR basestring
            OR pymel.core.PyNode

        :returns: Attribute at the given index.
        :rtype: pymel.core.PyNode

        :raises: KeyError, TypeError
        """
        if isinstance(index, int):
            return super(ChannelBox, self).__getitem__(index)

        elif isinstance(index, pm.general.Attribute):
            for attr in self:
                if index.shortName() == attr.shortName():
                    return attr
            raise KeyError(index)

        elif isinstance(index, basestring):
            for attr in self:
                if index in (attr.longName(), attr.shortName()):
                    return attr
            raise KeyError(index)

        else:
            errorMessage = '%s indices must be integers ' % self.__class__.__name__
            errorMessage += 'string or pymel.core.general.Attribute. '
            errorMessage += 'Gets %s' % type(index)
            raise TypeError(errorMessage)

    def __contains__(self, key):
        """y in x <-> x.__contains__(y)
        """
        if not isinstance(key, pm.general.Attribute):
            return super(ChannelBox, self).__contains__(key)
        else:
            for attr in self:
                if key.longName() == attr.longName():
                    return True
        return False

    def _filter(self):
        """Gets the node channelBox attribute(s) after the ignores filter.

        :returns: Pymel attributes.
        :rtype: generator of pymel.core.PyNode
        """
        for attr in self:
            short_name_in_ignores = attr.shortName() in self.ignores
            long_name_in_ignores = attr.longName() in self.ignores

            if not (short_name_in_ignores or long_name_in_ignores):
                yield attr

    @property
    def ignores(self):
        """x.ignores
        Gets the attribute(s) name to ignore during the process.

        :returns: Attribute(s) name.
        :rtype: Iterable of basestring
        """
        return self._ignores

    @ignores.setter
    def ignores(self, value):
        """x.ignore = value
        Sets the attribute(s) name to ignore during the process.

        :param value:
            OR Attribute(s) name.
            OR None
        :type value:
            OR Iterable of basestring
            OR None
        """
        if value is None:
            value = tuple()
        self._ignores = value

    def get(self, key, default=None):
        """x.get(key, default) -> x[key] if key in x, else default.

        :param key:
            OR Index number of the wanted attribute.
            OR Name of the wanted attribute.
            OR Pymel attribute.
        :type key:
            OR int
            OR basestring
            OR pymel.core.PyNode

        :param default: Object to return if key isn't in self.
        :type default: optional

        :returns:
            OR Pymel attribute at the given key.
            OR Default parameter value.
        :rtype:
            OR pymel.core.general.Attribute
            OR type(param default)

        :Example:
            from rigIO.channelBox import ChannelBox

            channelBox = ChannelBox('nodeName')
            channelBox.get('attributeName')
        """
        return self[key] if key in self else default

    def setDefault(self):
        """Set the node channelBox attributes(s) to there default value if there is.
        Log a warning message if a RuntimeError occur during the set value process.

        :Example:
            from rigIO.channelBox import ChannelBox

            channelBox = ChannelBox('nodeName')
            channelBox.setDefault()
        """
        for attr in self._filter():
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

    def connect(self, *destinations):
        """Connect current channelBox attribute(s) to the destination(s)
        channelBox attribute(s). Log a warning message if a RuntimeError occurs
        during the connection process.

        :param *destinations:
            OR Maya node name of the wanted destination(s).
            OR PyNode instance of the wanted destination(s).
            OR ChannelBox instance of the wanted destination(s).
        :type *destinations:
            OR str
            OR pymel.core.PyNode
            OR ChannelBox

        :Example:
            import pymel.core as pm
            from rigIO.channelBox import ChannelBox

            channelBox = ChannelBox('nodeName')

            # With str param type :
            sourceChannelBox.connect('destination_a', 'destination_b')

            # With pymel.core.PyNode param type :
            destinationPyNodeA = pm.PyNode('destination_a')
            destinationPyNodeB = pm.PyNode('destination_b')
            sourceChannelBox.connect(destinationPyNodeA, destinationPyNodeB)

            # With ChannelBox param type :
            destinationChannelBoxA = ChannelBox('destination_a')
            destinationChannelBoxB = ChannelBox('destination_b')
            sourceChannelBox.connect(destinationChannelBoxA, destinationChannelBoxB)
        """
        for channelBox in destinations:

            if not isinstance(channelBox, ChannelBox):
                channelBox = ChannelBox(channelBox)

            for attr in channelBox._filter():
                sourceAttr = self.get(attr)
                if sourceAttr:
                    try:
                        sourceAttr >> attr
                    except RuntimeError as error:
                        pm.warning(error.message[:-1])

    def disconnect(self):
        """Disconnect the node channelBox attribute(s).
        Log a warning error if there is no incoming connection(s).

        :Example:
            from rigIO.channelBox import ChannelBox

            channelBox = ChannelBox('nodeName')
            channelBox.disconnect()
        """
        for attr in self._filter():
            sourceAttr = attr.listConnections(source=True, plugs=True)
            sourceAttr = (sourceAttr or [None])[0]

            if sourceAttr and sourceAttr.isSource():
                sourceAttr // attr
            else:
                message = '%s has no incoming connections.' % attr.name()
                pm.warning(message)

    def setLocked(self, value):
        """Set the lock state of the node channelBox attribute(s).

        :param value:
            True  - Lock the channelBox attribute(s).
            False - Unlock the channelBox attribute(s).
        :type value: bool

        :Example:
            from rigIO.channelBox import ChannelBox

            channelBox = ChannelBox('nodeName')
            channelBox.setLocked(True)
            channelBox.setLocked(False)
        """
        for attr in self._filter():
            attr.setLocked(value)

    def clearKeys(self):
        """Delete the animation key(s) on the node chennelBox attribute(s).

        :Example:
            from rigIO.channelBox import ChannelBox

            channelBox = ChannelBox('nodeName')
            channelBox.clearKeys()
        """
        for attr in self._filter():
            pm.cutKey(attr)
