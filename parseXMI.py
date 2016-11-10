try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class Node:
    def __init__(self, el, root=None):
        self._el = el
        if root:
            self._root = root
        else:
            self._root = self

    def _el_to_node(self, el):
        return Node(el, self._root)

    def _els_to_nodes(self, els):
        return map(lambda x: self._el_to_node(x), els)

    def _get_children_by_el_attrib(self, attrib, val):
        nodes = filter(lambda x: x.get(attrib) == val, self._el)
        return self._els_to_nodes(nodes)

    def _get_el_by_relative_path_lst(self, el, relative_path_lst):
        if (len(relative_path_lst) == 0):
            return el
        else:
            for elChild in el:
                if (elChild.get('relid') == relative_path_lst[0]):
                    return self._get_el_by_relative_path_lst(elChild, relative_path_lst[1:])
            return None

    def _get_el_by_guid(self, el, guid):
        for elChild in el:
            if elChild.get('id') == guid:
                return elChild
            else:
                potential_el = self._get_el_by_guid(elChild, guid)
                if (potential_el is not None):
                    return potential_el
        return None

    def _get_partial_path(self, end, nlist):
        print self.get_relid(), end.get_relid()
        if self.get_relid() == end.get_relid():
            print "ab"
            return nlist
        children = self.get_children()
        if children:
            for child in children:
                print "ac"
                return child._get_partial_path(end, nlist+[self.get_relid()])
        # else:
        #     return None

    def is_meta_node(self):
        return el.get('isMeta') == 'true'

    def get_children(self, meta_type=None):
        if meta_type:
            # findall(tag) returns all immediate children with the given tag
            return self._els_to_nodes(self._el.findall(meta_type))
        else:
            return self._els_to_nodes(self._el)

    def get_attribute(self, attribute_name):
        return self._el.get('atr-' + attribute_name)

    def get_attribute_names(self):
        return map(lambda x: x[4:], filter(lambda x: x.startswith('atr-'), self._el.attrib))

    def get_relid(self):
        relid = self._el.get('relid')
        if (relid is None):
            return None
        else:
            return '/' + self._el.get('relid')

    def get_guid(self):
        return self._el.get('id')

    def get_node_by_relative_path(self, relative_path):
        relative_path_lst = filter(lambda x: len(x) > 0, relative_path.split('/'))
        el = self._get_el_by_relative_path_lst(self._el, relative_path_lst)
        if (el is None):
            return None
        else:
            return self._el_to_node(el)

    def get_node_by_guid(self, guid):
        el = self._get_el_by_guid(self._el, guid)
        if (el is None):
            return None
        else:
            return self._el_to_node(el)

    def get_child_by_relid(self, relid):
        nodes = self._get_children_by_el_attrib('relid', relid)
        if (len(nodes) == 0):
            return None
        else:
            return nodes[0]

    def get_child_by_guid(self, guid):
        nodes = self._get_children_by_el_attrib('id', guid)
        if (len(nodes) == 0):
            return None
        else:
            return nodes[0]

    def get_path(self):
        children = self._root.get_children()
        for child in children:
            print child.get_relid()
            path = child._get_partial_path(self, [child.get_relid()])
            if path:
                return path

    def print_node(self, tab):
        print tab, self.get_attribute('name')
        print tab, '  relid', self.get_relid()
        print tab, '  guid', self.get_guid()
        attribute_names = self.get_attribute_names()
        print tab, '  attributes'
        for attribute in attribute_names:
            print tab, '    ', attribute, self.get_attribute(attribute)

class Core:
    def __init__(self, file):
        tree = ET.parse(file)
        self._el = tree.getroot()
        self._root = Node(self._el)

    def _print_tree(self, node, tab):
        for child in node.get_children():
            child.print_node(tab)
            if (len(child.get_children()) > 0):
                print tab, '  children'
                self._print_tree(child, tab + '    ')

    def get_root_node(self):
        return self._root

    def get_all_meta_nodes(self):
        return map(lambda x: Node(x, self._root), filter(lambda x: x.get('atr-name') == x.tag, self._el.iter()))

    def get_node_by_path(self, path):
        return self._root.get_node_by_relative_path(path)

    def get_node_by_guid(self, guid):
        return self._root.get_node_by_guid(guid)

    def print_tree(self):
        self._print_tree(self._root, '')

if __name__ == '__main__':
    core = Core('FSMSignalFlow.xmi')
    rootNode = core.get_root_node()
    print rootNode.get_node_by_relative_path('/6/0')
    # print rootNode.getChildren()[1].getRelid()
    anode = rootNode.get_children()[1]
    bnode = anode.get_children()[1]
    # print bnode.getRelid()
    print bnode.get_path()
