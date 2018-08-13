import maya.cmds as mc
import maya.OpenMaya as om


def setupSublime(melPort=7001, pythonPort=7002):
    """Open the command ports to use sublime into maya using MayaSublime package
    from sublime.

    Keyword Arguments:
        melPort {int} -- (default: {7001})
            A port number to use for mel.
        pythonPort {int} -- (default: {7002})
            A port number to use for python.
    """

    for key, value in locals().items():
        # Close ports if they were already open under.
        try:
            mc.commandPort(name=":{}".format(value), close=True)
        except:
            pass
        # Open new ports.
        mc.commandPort(name=":{}".format(value), sourceType=key[:-4])

    om.MGlobal.displayInfo("Sublime is ready to use.")
