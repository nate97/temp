from panda3d.core import LVector4f, DecalEffect, NodePath

import DNAError
import DNAGroup
import DNAUtil


class DNADoor(DNAGroup.DNAGroup):
    COMPONENT_CODE = 17

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        doorNodePath.setColor(color, 0)
        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.flattenStrong()
        leftHole.setName('doorFrameHoleLeft')
        leftHoleGeom = leftHole.find('**/+GeomNode')
        leftHoleGeom.setName("doorFrameHoleLeftGeom")
        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.flattenStrong()
        rightHoleGeom = rightHole.find('**/+GeomNode')
        rightHoleGeom.setName('doorFrameHoleRightGeom')
        rightHole.setName('doorFrameHoleRight')
        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.flattenStrong()
        leftDoor.setName('leftDoor')
        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.flattenStrong()
        rightDoor.setName('rightDoor')
        doorFlat = doorNodePath.find('door_*_flat')
        doorFlat.setEffect(DecalEffect.make())
        doorFlat.flattenStrong()
        leftHole.wrtReparentTo(doorFlat, 0)
        rightHole.wrtReparentTo(doorFlat, 0)

        if not leftHoleGeom.getNode(0).isGeomNode():
            leftHoleGeom = leftHoleGeom.find('**/+GeomNode')

        if not rightHoleGeom.getNode(0).isGeomNode():
            rightHoleGeom = rightHoleGeom.find('**/+GeomNode')

        leftHoleGeom.setEffect(DecalEffect.make())
        rightHoleGeom.setEffect(DecalEffect.make())

        rightDoor.wrtReparentTo(parentNode, 0)
        leftDoor.wrtReparentTo(parentNode, 0)

        rightDoor.setColor(color, 0)
        leftDoor.setColor(color, 0)

        rightDoor.hide()
        leftDoor.hide()

        leftHole.setColor((0, 0, 0, 1), 0)
        rightHole.setColor((0, 0, 0, 1), 0)

        rightHole.hide()
        leftHole.hide()

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_' + block)

        doorNodePath.flattenMedium()

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        frontNode = nodePath.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError.DNAError('DNADoor code ' + self.code + ' not found in DNAStorage')
        doorNode = node.copyTo(frontNode, 0)
        doorNode.flattenMedium()
        doorOrigin = nodePath.find('**/*door_origin')
        block = dnaStorage.getBlock(nodePath.getName())
        DNADoor.setupDoor(doorNode, nodePath, doorOrigin, dnaStorage, block, self.getColor())
        storeNp = NodePath('doorPosHpr')
        storeNp.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        dnaStorage.storeBlockDoor(block, storeNp)
