import uuid


class Node:
    def __init__(self, name, identifier=None, parent=None, text="", callback=None, final=False):
        self._identifier = (str(uuid.uuid1()) if identifier is None else str(identifier))
        self.name = name
        self.text = text
        self.final = final
        self._parent = parent
        self._children = []
        self._callbacks = [] if callback is None else [].append(callback)

    @property
    def identifier(self):
        return self._identifier

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        if value is not None:
            self._parent = value

    @property
    def children(self):
        return self._children

    def child(self, identifier):
        for child in self._children:
            if child.identifier is identifier:
                return child
        return None

    def add_child(self, identifier):
        self._children.append(identifier)

    def register_callback(self, callback):
        self._callbacks.append(callback)
