from collections import defaultdict
from Tree import Node,Tree
from constants import TRUE,FALSE,UNKNOWN

class PN:
    def __init__(self,name,root,evaluate,result,get_pn_dpn,max_nodes,delete_subtrees=False,immediateEvaluation=True):
        self.pn_tree = Tree()
        self.name = name
        self.evaluate = evaluate
        self.result = result
        self.get_pn_dpn = get_pn_dpn 
        self.max_nodes = max_nodes
        self.delete_subtrees = delete_subtrees
        self.immediateEvaluation = immediateEvaluation

        self.root = root
        self.pn_tree.set_root(self.root)
        self.eval_count = 0
        self.terminated = False

    def terminate(self):
        self.terminated = True
        
    def evaluate_node(self, node):
        self.evaluate(node)
        self.eval_count+=1

    def reset(self,node):
        self.eval_count = 0
        self.root = node
        self.pn_tree.clear()
        self.pn_tree.set_root(self.root)
    
    def set_second_level(self,evaluate):
        pass
    def set_evaluate(self,evaluate):
        self.evaluate = evaluate
    def set_limit(self,max_nodes):
        self.max_nodes = max_nodes
    def get_size(self):
        return self.pn_tree.node_count
    def get_node_count(self):
        return self.pn_tree.node_count+self.pn_tree.deleted_count
    def perform_search(self):
        if self.immediateEvaluation:
            self.evaluate_node(self.root)
        self.set_pn_dpn(self.root)
        current_node = self.root
        while self.root.pn != 0 and self.root.dpn != 0 and self.pn_tree.node_count<=self.max_nodes and not self.terminated:
            most_proving = self.select_most_proving_node(current_node)
            if not self.immediateEvaluation:
                self.evaluate_node(most_proving)
                self.set_pn_dpn(most_proving)
            self.expand_node(most_proving)
            current_node = self.update_ancestors(most_proving)
        return self.result(self)

    # Calculating proof and disproof numbers
    def set_pn_dpn(self,node):
        # Internal Node
        if node.expanded:
            # AND Node
            # PN = sum of children PN; DPN = minimum of children DPN
            if node.node_type == "AND":
                node.pn = sum(c.pn for c in node.children)
                node.dpn = min(c.dpn for c in node.children)
            # OR Node
            # PN = minimum of children PN; DPN = sum of children DPN
            else:
                node.pn = min(c.pn for c in node.children)
                node.dpn = sum(c.dpn for c in node.children)
        # Leaf node
        else:
            evaluation = node.value
            # Lost
            if evaluation == FALSE:
                node.pn = float("inf")
                node.dpn = 0
            # Won
            elif evaluation == TRUE:
                node.pn = 0
                node.dpn = float("inf")
            # Unknown
            elif evaluation == UNKNOWN:
                node.pn, node.dpn = self.get_pn_dpn(node)

    def select_most_proving_node(self,node):
        while node.expanded:
            # Lowest DPN
            if node.node_type == "AND":
                vals = [c.dpn for c in node.children]
            # Lowest PN
            else:
                vals = [c.pn for c in node.children]
            node = node.children[vals.index(min(vals))]
        return node

    def expand_node(self,node):
        if node.pn == 0 or node.dpn == 0:return
        # Check whether evaluation added children to node
        if node.expanded:return
        # generate all children
        child_type = "AND" if node.node_type == "OR" else "OR"
        for a in node.state.allowed_actions():
            new_state = node.state.perform_action(a)
            # Node(Type,State,Parent,Action)
            child_node = Node(node_type=child_type,state=new_state,parent=node,depth=node.depth+1,action=a)
            self.add_child(child_node,node)

            if self.immediateEvaluation:
                self.evaluate_node(child_node)
            self.set_pn_dpn(child_node)
            if child_node.pn == 0 and node.node_type == "OR":break     # won
            if child_node.dpn == 0 and node.node_type == "AND":break    # lost
        node.expanded = True

    def update_ancestors(self,node):
        while True:
            old_pn = node.pn
            old_dpn = node.dpn
            # Check in case of delayed evaluation
            if old_pn == 0 or old_dpn == 0:
                if node == self.root:
                    return self.root
                node = node.parent 
                continue
            self.set_pn_dpn(node)
            # No change on the path
            if node.pn == old_pn and node.dpn == old_dpn:
                return node
            # delete disproved subtrees
            if self.delete_subtrees and (node.pn == 0 or node.dpn == 0):
                self.delete_subtree(node)
            
            if node == self.root:
                return self.root             
            node = node.parent
        return node
    def delete_subtree(self,node):
        self.pn_tree.delete_subtree(node)  

    def add_child(self,child_node,node):
        self.pn_tree.add_child(child_node,node)