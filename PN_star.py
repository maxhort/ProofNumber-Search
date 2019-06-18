from Tree import Node

class PN_star:
    def __init__(self,name,root,evaluate,result,get_pn,transposition_table,max_table_size):
        self.name = name
        self.evaluate = evaluate
        self.result = result
        self.get_pn = get_pn
        self.max_table_size = max_table_size
        self.root = root
        self.TT = transposition_table
        self.eval_count = 0
    def evaluate_node(self, node):
        self.evaluate(node)
        self.eval_count+=1
    def set_evaluate(self,evaluate):
        self.evaluate = evaluate
    def get_size(self):
        return self.TT.size()
    def get_node_count(self):
        return self.eval_count
    def reset(self,root):
        self.eval_count = 0
        self.root = root
        self.TT.reset()

    # Iterative deepening at the root
    def perform_search(self):
        # initialize pn threshold at the root
        self.root.pn = 1
        while self.root.pn!=0 and self.root.pn!=float('inf') and self.TT.size()<self.max_table_size:
            self.expand(self.root,self.root.pn)
        #return self.root
        return self.result(self)
        
    # find entry in transposition table
    def findtable(self,node):
        res = self.TT.lookup(node.state.hashcode,node.state.hashkey)
        return self.get_pn(node) if res is None else res["pn"]
    
    # Replacement scheme: keep the deepest evaluated node
    def putintable(self,node,depth):
        self.TT.add_entry(node.state.hashcode,self.generate_entry(node,node.state.hashkey,depth))

    # size is equal to depth
    def generate_entry(self,node,hashkey,size):
        return {"pn":node.pn, "size":size,"hashkey":hashkey}

    # expand leaf nodes of pst rooted at node
    def expand(self,node,pn_threshold):
        c = self.findtable(node)
        # IF node already solved or pn exceeds threshold
        if c==0 or c>pn_threshold:
            node.pn = c
            return
        # Initialize PN as 1
        #if node.pn == None: node.pn = 1

        # If node has no successors
        # check if game is finished
        self.evaluate_node(node)
        result = node.value
        if result == 0:
            node.pn = float('inf')
            self.putintable(node,pn_threshold)
            return
        elif result == 1:
            node.pn = 0
            self.putintable(node,pn_threshold)
            return
        # Stored in transposition table to detect cycles
        self.putintable(node,pn_threshold)

        if node.node_type == "OR":
            # Recursive call of successor and nodes
            min_child = float('inf')
            for a in node.state.allowed_actions():
                new_state = node.state.perform_action(a)
                child_node = Node(node_type="AND",state=new_state,parent=node,depth=node.depth+1,action=a)
                self.expand(child_node,pn_threshold)
                min_child = min(min_child,child_node.pn)
                if child_node.pn == 0:
                    break
            node.pn = min_child
            self.putintable(node,pn_threshold)
            return

        if node.node_type == "AND":
            # Dynamic evaluation
            child_pn = []
            for a in node.state.allowed_actions():
                new_state = node.state.perform_action(a)
                child_node = Node(node_type="OR",state=new_state,parent=node,depth=node.depth+1,action=a)
                entry = self.findtable(child_node)
                child_pn.append(entry)
            if sum(child_pn)>pn_threshold:
                node.pn = sum(child_pn)
                self.putintable(node,pn_threshold)
                return

            # The recursive call of the successor OR nodes
            for i,a in enumerate(node.state.allowed_actions()):
                new_state = node.state.perform_action(a)
                # Recursive iterative deepening
                child_node = Node(node_type="OR",state=new_state,parent=node,depth=node.depth+1,action=a)
                child_node.pn = 1
                while child_node.pn != 0:
                    self.expand(child_node,child_node.pn)
                    # in case child is solved
                    if child_node.pn == 0: break

                    # if unsolved within threshold
                    child_pn[i] = child_node.pn
                    if sum(child_pn)>pn_threshold:
                        node.pn = sum(child_pn)
                        self.putintable(node,pn_threshold)
                        return

            # All successor OR nodes of node n are solved
            node.pn = 0
            self.putintable(node,pn_threshold)
            return
                
            
        
        