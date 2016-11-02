import xml.etree.ElementTree as ET

class Node:
    def __init__(self, el, root):
        self._root = root
        self._el = el

    def _elToNode(self, el):
        return Node(el, self._root)

    def _elsToNodes(self, els):
        return map(lambda x: self._elToNode(x), els)

    def _getElAttrib(self, el, attr):
        return el.attrib.get(attr)

    def _isElMeta(self, el):
        return self._getElAttrib(el, 'isMeta') == 'true'

    # def _isElMetaType(self, el, metaType):
        # return self._getElAttrib

    def isMetaNode(self):
        return self._isElMeta(self._el)

    def getChildren(self, metaType=None):
        if metaType:
            # return self._elsToNodes(filter(lambda x: self._isElMeta(x), els))
            return []
        else:
            return self._elsToNodes(self._el)

    def getAttribute(self, attributeName):
        return self._getElAttrib(self._el, attributeName)

    def getAttributeNames(self):
        return list(self._el.attrib)

    def getRelid(self):
        return self.getAttribute('relid')

    def getGuid(self):
        return self.getAttribute('id')

def readFile(file):
    tree = ET.parse(file)
    return tree.getroot()

if __name__ == '__main__':
    rootEl = readFile('FSMSignalFlow.xmi')
    rootNode = Node(rootEl, None)
    print rootNode.getChildren()[2].getGuid()
