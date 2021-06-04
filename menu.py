from menu_list import MenuList


class Menu:
    def __init__(self):
        self._menu = MenuList()

    def getChildren(self, identifier):
        ids = self._menu.tree[identifier].children
        return [self._menu.tree[node] for node in ids]

    def getChildrenText(self, identifier):
        nodes = self.getChildren(identifier)
        return [child.text for child in nodes]

    def getParent(self, identifier):
        return self._menu.tree[identifier].parent

    def callCallback(self, identifier):
        self._menu.tree[identifier].call_callback()

    def registerCallback(self, identifier, callback):
        self._menu.tree[identifier].register_callback(callback)


if __name__ == "__main__":
    men = Menu()
    te = men.getParent("led_root")
    print(te)
