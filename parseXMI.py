import pprint

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

class Node:
    def __init__(self, el, root=None):
        self._atr_prefix = 'atr-'
        self._ptr_prefix = 'rel-'
        self._invptr_prefix = 'invrel-'
        self._set_prefix = 'set-'
        self._el = el
        if root:
            self._root = root
        else:
            self._root = self

    def _el_to_node(self, el):
        return Node(el, self._root)

    def _els_to_nodes(self, els):
        return map(lambda x: self._el_to_node(x), els)

    def get_root(self):
        return self._root

    def _get_children_by_el_attrib(self, attrib, val):
        nodes = filter(lambda x: x.get(attrib) == val, self._el)
        return self._els_to_nodes(nodes)

    def _get_el_by_relative_path_lst(self, el, relative_path_lst):
        if len(relative_path_lst) == 0:
            return el
        else:
            for elChild in el:
                if elChild.get('relid') == relative_path_lst[0]:
                    return self._get_el_by_relative_path_lst(elChild, relative_path_lst[1:])
            return None

    def _get_el_by_guid(self, el, guid):
        for elChild in el:
            if elChild.get('id') == guid:
                return elChild
            else:
                potential_el = self._get_el_by_guid(elChild, guid)
                if potential_el is not None:
                    return potential_el
        return None

    def _get_path(self, curEl, findEl, path):
        if curEl is findEl:
            return path
        else:
            for child in curEl:
                childPath = self._get_path(child, findEl, path + '/' + child.get('relid'))
                if childPath is not None:
                    return childPath
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
        return self._el.get('isMeta') == 'true'

    def get_children(self, meta_type=None):
        if meta_type is not None:
            # findall(tag) returns all immediate children with the given tag
            return self._els_to_nodes(self._el.findall(meta_type))
        else:
            return self._els_to_nodes(self._el)

    def get_attribute(self, attribute_name):
        prefix = self._atr_prefix
        return self._el.get(prefix + attribute_name)

    def get_attribute_names(self):
        prefix = self._atr_prefix
        return map(lambda x: x[len(prefix):], filter(lambda x: x.startswith(prefix), self._el.attrib) )

    def get_relid(self):
        relid = self._el.get('relid')
        if relid is None:
            return None
        else:
            return '/' + relid

    def get_guid(self):
        return self._el.get('id')

    def get_node_by_relative_path(self, relative_path):
        relative_path_lst = filter(lambda x: len(x) > 0, relative_path.split('/'))
        el = self._get_el_by_relative_path_lst(self._el, relative_path_lst)
        if el is None:
            return None
        else:
            return self._el_to_node(el)

    def get_node_by_guid(self, guid):
        el = self._get_el_by_guid(self._el, guid)
        if el is None:
            return None
        else:
            return self._el_to_node(el)

    def get_child_by_relid(self, relid):
        nodes = self._get_children_by_el_attrib('relid', relid)
        if len(nodes) == 0:
            return None
        else:
            return nodes[0]

    def get_child_by_guid(self, guid):
        nodes = self._get_children_by_el_attrib('id', guid)
        if len(nodes) == 0:
            return None
        else:
            return nodes[0]

    def get_path(self):
        return self._get_path(self._root._el, self._el, '')

    def get_pointer_guid(self, pointer_name):
        prefix = self._ptr_prefix
        for attrib in self._el.attrib:
            if attrib.startswith(prefix + pointer_name):
                return self._el.attrib[attrib]
        return None

    def get_pointer_node(self, pointer_name):
        pointer_guid = self.get_pointer_guid(pointer_name)
        if pointer_guid is not None:
            return self._root.get_node_by_guid(pointer_guid)
        else:
            return None

    def get_pointer_path(self, pointer_name):
        pointer_node = self.get_pointer_node(pointer_name)
        if pointer_node is not None:
            return pointer_node.get_path()
        else:
            return None

    def get_pointer_names(self):
        prefix = self._ptr_prefix
        return map(lambda x: x[len(prefix):x.rfind('-')], filter(lambda x: x.startswith(prefix), self._el.attrib) )

    def get_base(self):
        base_guid = self._el.get('base')
        if base_guid:
            return self._root.get_node_by_guid(base_guid)
        else:
            return None

    def get_collection_names(self):
        prefix = self._invptr_prefix
        return map(lambda x: x[len(prefix):x.rfind('-')], filter(lambda x: x.startswith(prefix), self._el.attrib) )

    def get_collection_guids(self):
        prefix = self._invptr_prefix
        return map(lambda x: self._el.get(x), filter(lambda x: x.startswith(prefix), self._el.attrib) )

    def get_collection_nodes(self):
        return map(lambda x: self._root.get_node_by_guid(x), self.get_collection_guids())

    def get_collection_paths(self):
        return map(lambda x: x.get_path(), self.get_collection_nodes())

    def get_set_names(self):
        prefix = self._set_prefix
        return map(lambda x: x[len(prefix):x.rfind('-')], filter(lambda x: x.startswith(prefix), self._el.attrib) )

    def get_members_guids(self, set_name):
        prefix = self._set_prefix
        for attrib in self._el.attrib:
            if attrib.startswith(prefix + set_name):
                return self._el.attrib[attrib].split(' ')
        return None

    def get_members_nodes(self, set_name):
        members_guids = self.get_members_guids(set_name)
        if members_guids is not None:
            return map(lambda x: self._root.get_node_by_guid(x), members_guids)
        else:
            return None

    def get_members_paths(self, set_name):
        members_nodes = self.get_members_nodes(set_name)
        if members_nodes is not None:
            return map(lambda x: x.get_path(), members_nodes)
        else:
            return None

    def get_meta_node(self):
        if self.is_meta_node():
            return self
        else:
            return self.get_base()

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
        return map(lambda x: Node(x, self._root), filter(lambda x: x.get('isMeta') == 'true', self._el.iter()))

    def get_node_by_path(self, path):
        return self._root.get_node_by_relative_path(path)

    def get_node_by_guid(self, guid):
        return self._root.get_node_by_guid(guid)

    def print_tree(self):
        self._print_tree(self._root, '')

def mini_project_2(root_node):
    structure = dict()
    structure['3-isMeta'] = root_node.is_meta_node()
    structure['4-metaType'] = root_node.get_meta_node().get_attribute('name')
    for attr_name in root_node.get_attribute_names():
        structure['1-' + attr_name] = root_node.get_attribute(attr_name)
    for ptr_name in root_node.get_pointer_names():
        structure['2-' + ptr_name] = root_node.get_pointer_node(ptr_name).get_attribute('name')
    children = root_node.get_children()
    if len(children) > 0:
        structure['5-children'] = []
        for child in children:
            structure['5-children'].append(mini_project_2(child))
    return structure

def mini_project_2_meta(meta_nodes):
    res = []
    for meta_node in meta_nodes:
        attr = dict()
        attr['name'] = meta_node.get_attribute('name')
        attr['path'] = meta_node.get_path()
        attr['nbrOfChildren'] = len(meta_node.get_children())
        base = meta_node.get_base()
        attr['base'] = None
        if base is not None:
            attr['base'] = base.get_attribute('name')
        res.append(attr)
    return res

if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    core = Core('FSMSignalFlow.xmi')
    root_node = core.get_root_node()
    # core.print_tree()

    # print
    # print

    structure = dict()
    structure['1-name'] = 'ROOT'
    structure['5-children'] = []
    for child in root_node.get_children():
        structure['5-children'].append(mini_project_2(child))
    pp.pprint(structure)
    print
    pp.pprint(mini_project_2_meta(core.get_all_meta_nodes()))
