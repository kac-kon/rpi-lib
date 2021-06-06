from components.menu.tree_node import Node


class Tree:
    def __init__(self):
        self.nodes = []

    def get_index(self, position):
        index = None
        for index, node in enumerate(self.nodes):
            if node.identifier == position:
                break
        return index

    def create_node(self, name, identifier=None, parent=None, text="", callback=None, final=False):
        node = Node(name, identifier, parent, text=text, callback=callback, final=final)
        self.nodes.append(node)
        self._update_parents_children(parent, identifier)

    def _update_parents_children(self, position, identifier):
        if position is None:
            return
        else:
            self[position].add_child(identifier)

    def __getitem__(self, item) -> Node:
        return self.nodes[self.get_index(item)]

    def __setitem__(self, key, value):
        self.nodes[self.get_index(key)] = value

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, item):
        return [node.identifier for node in self.nodes if node.identifier is item]
