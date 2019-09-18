import sys 

from lxml import html

def main(argv):
    origin_path = argv[1]

    try:
        origin_tree = html.parse(origin_path)
    except:
        print('Invalid original file path!')
        return 0 

    origin_root = origin_tree.getroot()

    def node_by_id(node, xid):
        def rec_find(node):
            if 'id' in node.keys() and node.attrib['id'] == xid:
                return (node, node.tag)
            if node.getchildren():
                for child in node.getchildren():
                    res = rec_find(child)
                    if res != None:
                        return (res[0], node.tag + '>' + res[1])
            return None
        return rec_find(node)

    ok_button, path = node_by_id(origin_root, "make-everything-ok-button")

    other_path = argv[2]

    try:
        other_tree = html.parse(other_path)
    except:
        print('Invalid original file path!')
        return 0

    other_root = other_tree.getroot()

    def node_by_node(node, xnode):
        def rec_find(node):
            new_attrs = 0
            for k in xnode.keys():
                if k in node.keys() and node.attrib[k] == xnode.attrib[k]:
                    new_attrs += 1
            if node.tag == xnode.tag:
                new_attrs += 1
            if node.text == xnode.text:
                new_attrs += 1

            if node.getchildren():
                max_attrs = new_attrs
                max_node = node
                max_path = ''
                for child in node.getchildren():
                    cur_node, cur_attrs, cur_path = rec_find(child)
                    if cur_attrs > max_attrs:
                        max_node, max_attrs, max_path = cur_node, cur_attrs, cur_path
                return  max_node, max_attrs, node.tag + '>' + max_path
            return node, new_attrs, node.tag
        return rec_find(node)

    _, _, path = node_by_node(other_root, ok_button)

    print(path)

if __name__ == '__main__':
    main(sys.argv)