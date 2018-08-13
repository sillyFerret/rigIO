# Maya libraries
import maya.cmds as mc
import maya.api.OpenMaya as om


def subdivideJoint(start, end, subdiv, hierarchy=True):
    """Add the desired number of joint(s) in between two given joints.

    Arguments:
        start {str} -- Name of the start joint.
        end {str} -- Name of the end joint.
        subdiv {int} -- Desired number of joint(s) in between the start and end
            joint.

    Keyword Arguments:
        hierarchy {bool} -- (default: {True})
            If true, will place the given joints in hierarchy, from start to end.

    Returns:
        list -- Name of the created joints including the given start and end joints.
            Ex: [u'startjoint', u'joint1', u'joint2', u'joint3', u'endjoint']
    """
    # Initialize the return value.
    jnts = [start]

    # Get the worldSpace pntition of the given joints
    startPnt = mc.xform(start, q=True, ws=True, t=True)
    endPnt = mc.xform(end, q=True, ws=True, t=True)

    # Do the Radius math
    startR = mc.getAttr(start+'.radius')
    endR = mc.getAttr(end+'.radius')
    stepR = (endR-startR)*(1.0/(subdiv+1))

    # Do the vector math
    startV = om.MVector(*startPnt)
    endV = om.MVector(*endPnt)
    stepV = (endV-startV) * 1.0/(subdiv+1)

    # Create and place the joints
    for i in range(subdiv):
        jnt = mc.createNode('joint')
        pnt = startV+(stepV*(i+1))
        mc.xform(jnt, ws=True, t=(pnt.x, pnt.y, pnt.z))
        mc.setAttr(jnt+'.radius', startR+(stepR*(i+1)))
        jnts.append(jnt)

    # Parent the joints in the right hierarchy.
    jnts.append(end)
    if end in mc.listRelatives(start) and hierarchy:
        for i, jnt in enumerate(jnts[1:]):
            mc.parent(jnt, jnts[i])

    return jnts
