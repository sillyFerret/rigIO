# Python libraries
import os
import re
import json
# Maya libraries
import maya.cmds as mc
# RigIO libraries
from constants import FORMAT, TAGS, TAG_NUM, SIDES, EXCEPTIONS, TYPES


class AbstractNameConvention(object):

    def __init__(self, name):
        super(AbstractNameConvention, self).__init__()
        self.name = name


    @property
    def niceName(self):
        niceName = self.name.split(':')[-1]
        return niceName.split('|')[-1]


    @property
    def split(self):
        """ x.split <==> x.niceName.split('_')
        """
        return self.niceName.split('_')


    @property
    def isFormat(self):
        """Check if the given name has the right number of tags.

        :rtype: {bool}
        """
        return len(self.split) == TAG_NUM


    @property
    def tags(self):
        """Returns a dictionary where the keys are the _TAGS and the values are
            the corresponding value for each tags of the given name.

        :rtype: {dict{string:string}}
        """
        if not self.isFormat:
            return {}

        rtn = {}
        for tag in TAGS:
            rtn[tag] = self.__getattribute__(tag)

        return rtn


    @property
    def isValid(self):
        """Check if the given name is valid.
        :rtype: {bool}
        """

        for tag in TAGS:
            if not self.__getattribute__(tag):
                return False

        return True


    @staticmethod
    def splitCamelCase(strArg):
        """Split a given string according to the rules of the camel case.

        :param strArg: String to split.
        :type strArg: str

        :returns: List containing the split string.
        :rtype: {list(str)}
        """
        return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|[0-9]+', strArg)


    @staticmethod
    def joinCamelCase(*strArgs):
        return strArgs[0]+''.join(
            [i.replace(i[0], i[0].upper()) for i in strArgs[1:]])


class NameConvention(AbstractNameConvention):

    def __init__(self, name, side=None, info=None, type=None, num=None):
        """x.__init__(name) <==> x(name)
        """
        super(NameConvention, self).__init__(name)
        _side = side
        _info = info
        _type = type
        _num  = num

    @property
    def side(self):

        if not self.isFormat:
            side = self.split[0][0]
        else :
            side = self.split[TAGS.index('side')]

        if side in __SIDES.values():
            return side

    @property
    def info(self):

        if not self.isFormat:
            split = self.splitCamelCase(self.niceName)
            num = ([i for i in split if i.isdigit()] or [None])[-1]
            if num:
                split.remove(num)
            info = self.joinCamelCase(*split)

        else:
            info = self.split[TAGS.index('info')]

    # Type
    def getType(self):
        if not self.isFormat:
            return 'none'
        return self.split[TAGS.index('Type')]


    def isValidType(self):
        if not self.isFormat:
            return
        pass

    # Num
    def getNum(self):
        if not self.isFormat:
            return '1'
        return self.split[TAGS.index('Num')]


    def isValidNum(self):
        if not self.isFormat:
            return
        pass
