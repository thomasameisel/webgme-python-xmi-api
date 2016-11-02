import xml.etree.ElementTree as ET

class Node:
    def __init__(self, el, root=None):
        self._el = el
        if root:
            self._root = root
        else:
            self._root = self

    def _elToNode(self, el):
        return Node(el, self._root)

    def _elsToNodes(self, els):
        return map(lambda x: self._elToNode(x), els)

    def _getElAttrib(self, el, attr):
        return el.get(attr)

    def _isElMeta(self, el):
        return self._getElAttrib(el, 'isMeta') == 'true'

    def _getNodesByElAttrib(self, attrib, val):
        nodes = filter(lambda x: self._getElAttrib(x, attrib) == val, self._el)
        if (len(nodes) == 0):
            return None
        else:
            return self._elsToNodes(nodes)

    def isMetaNode(self):
        return self._isElMeta(self._el)

    def getChildren(self, metaType=None):
        if metaType:
            # findall(tag) returns all immediate children with the given tag
            return self._elsToNodes(self._el.findall(metaType))
        else:
            return self._elsToNodes(self._el)

    def getAttribute(self, attributeName):
        return self._getElAttrib(self._el, 'atr-' + attributeName)

    def getAttributeNames(self):
        return map(lambda x: x[4:], filter(lambda x: x.startswith('atr-'), self._el.attrib))

    def getRelid(self):
        return '/' + self._getElAttrib(self._el, 'relid')

    def getGuid(self):
        return self._getElAttrib(self._el, 'id')

    def getNodeByPath(self, path):
        return self._getNodesByElAttrib('relid', path[1:])[0]

    def getNodeByGuid(self, guid):
        return self._getNodesByElAttrib('id', guid)[0]

class Core:
    def __init__(self, file):
        tree = ET.parse(file)
        self._el = tree.getroot()
        self._root = Node(self._el)

    def getRootNode(self):
        return self._root

    def getAllMetaNodes(self):
        return map(lambda x: Node(x, self._root), filter(lambda x: x.get('atr-name') == x.tag, self._el.iter()))

if __name__ == '__main__':
    core = Core('FSMSignalFlow.xmi')
    rootNode = core.getRootNode()
    print core.getAllMetaNodes()
