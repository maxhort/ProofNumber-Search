class Node:
    def __init__(self,node_type,state,parent,depth,action=None):
        self.id = 0
        self.state = state
        self.node_type = node_type
        self.pn = 1
        self.dpn = 1
        self.children = []
        self.parent = parent
        self.expanded = False
        self.value = 2
        self.action = action
        self.evaluated = False
        self.depth = depth
        self.is_draw = False
    def set_id(self,id):
        self.id = id
    def set_parent(self,parent):
        self.parent = parent
    def add_child(self, node):
        self.children.append(node)
        node.parent = self

    def delete_children(self,delete=False):
        num_children = len(self.children)
        deleted_children = sum(c.delete_children(delete = True) for c in self.children)
        self.children.clear()
        # self.children = []
        # if delete:
        #     del self
        return num_children + deleted_children
class Tree:
    def __init__(self):
        self.current_id = 1
        self.node_count = 0
        self.deleted_count = 0
        self.root = None

    def clear(self):
        self.current_id = 1
        self.node_count = 0
        self.deleted_count = 0
        self.root = None

    def set_root(self,node):
        self.root = node
        node.set_id(self.current_id)
        self.current_id += 1
        self.node_count += 1

    def add_child(self,node,parent):
        node.set_parent(parent)
        parent.add_child(node)
        node.set_id(self.current_id)
        self.current_id += 1
        self.node_count += 1

    def delete_subtree(self,node):
        deleted = node.delete_children()
        self.deleted_count += deleted
        self.node_count -= deleted
