class Node(object):
    def __init__(self, node_id, parent=None, value=None):
        self.id = node_id
        self.value = value
        self.parent = parent
        self.children = []

    def create_child(self, node_id=None):
        new_node = Node(node_id, self)
        self.children.append(new_node)
        return new_node

    def set_value(self, value):
        self.value = value

    def __str__(self):
        return str(self.id) + ": " + str(self.value)
