## API Calls

initialize(filename) - returns root Node

Node class
  - getNodeByPath(path) - return child with the path
  - getChildren() - return list of immediate children
  - getChildren(metaType) - return list of immediate children of metaType
  - getAttribute(attributeName) - return attribute of node
  - getAttributeNames() - return list of attribute names
  - getNodeByGuid(guid) - return child node with guid
  - getPointerNames() - return list of pointer names (rel)
  - getPointer(pointerName) - return target node of given pointer
  - getBase() - return base node or None
  - getCollection(pointerName) - return list of reverse pointers (invrel)
  - getRelid() - return relative id of node
  - getPath() - return path of node
  - getGuid() - return guid of node
  - isMetaNode() - return if node is meta
  - getAllMetaNodes() - return list of all meta nodes

  - ref to element in element tree (etree) (from xmi) (\_el)
  - ref to root element (\_root)

Done
  - getNodeByPath(path) - return child with the path
  - getChildren() - return list of immediate children
  - getChildren(metaType) - return list of immediate children of metaType
  - getAttribute(attributeName) - return attribute of node
  - getAttributeNames() - return list of attribute names
  - getNodeByGuid(guid) - return child node with guid
  - getRelid() - return relative id of node
  - getGuid() - return guid of node
  - isMetaNode() - return if node is meta
  - getAllMetaNodes() - return list of all meta nodes

  - ref to element in element tree (etree) (from xmi) (\_el)
  - ref to root element (\_root)

TODO: sets
