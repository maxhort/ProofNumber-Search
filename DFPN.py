from Tree import Node

class DFPN:
    def __init__(self,name,root,evaluate,result,get_pn_dpn,transposition_table,max_table_size,e=None,second_level=None):
        self.name = name
        self.evaluate = evaluate
        self.result = result
        self.get_pn_dpn = get_pn_dpn

        self.e = e
        self.max_table_size = max_table_size
        self.root = root
        self.TT = transposition_table
        self.second_level = second_level
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
        self.TT.reset()
    def set_evaluate(self,evaluate):
        self.evaluate = evaluate
    def set_second_level(self,evaluate):
        self.second_level = evaluate
    def set_limit(self,max_nodes):
        self.max_table_size = max_nodes
    def get_size(self):
        return self.TT.size()
    def get_node_count(self):
        return self.eval_count
    # Iterative deepening at the root
    def perform_search(self):
        # initialize pn threshold at the root
        self.root.pn = float('inf')
        self.root.dpn = float('inf')
        self.expand(self.root)
        return self.result(self)
    
    # check if node is in transposition table
    def in_table(self,node):
        return self.TT.in_table(node.state.hashcode,node.state.hashkey)
    # find entry in transposition table
    def findtable(self,node):
        res = self.TT.lookup(node.state.hashcode,node.state.hashkey)
        return self.get_pn_dpn(node) if res is None else (res["pn"],res["dpn"])
    
    # Put data in TT
    def putintable(self,node,size=1):
        self.TT.add_entry(node.state.hashcode,self.generate_entry(node,node.state.hashkey,size))

    # board, pn, best_move, solution length, size pst
    def generate_entry(self,node,hashkey,size):
        return {"pn":node.pn, "dpn":node.dpn,"hashkey":hashkey,"size":size}

    # expand leaf nodes of pst rooted at node
    def expand(self,node):
        def proof_sum(children):
            return sum(c.pn for c in children)
        def disproof_min(children):
            return min(c.dpn for c in children)
        #print (node.proof,node.disproof,node.state.board)
        proof,disproof = self.findtable(node)
        # Terminate searching if not necessary, limit reached of TT limit reached
        if node.pn<=proof or node.dpn<=disproof or self.max_table_size<=self.get_size() or self.terminated:
            node.pn = proof
            node.dpn = disproof
            return
        # If node has no successors
        # check if game is finished
        self.evaluate_node(node)
        result = node.value
        if (result==1 and node.node_type == "AND") or (result==0 and node.node_type == "OR"):
            node.pn = float('inf')
            node.dpn = 0
            self.putintable(node)
            return
        elif result in (1,0):
            node.pn = 0
            node.dpn = float('inf')
            self.putintable(node)
            return

        # Stored in transposition table to detect cycles
        self.putintable(node)        
        

        children = []
        # generate all children
        for a in node.state.allowed_actions():
            new_state = node.state.perform_action(a)
            # find children in TT
            child_type = "AND" if node.node_type == "OR" else "OR"
            #child_node = Node(child_type,new_state,None,a)
            child_node = Node(node_type=child_type,state=new_state,parent=node,depth=node.depth+1,action=a)
            child_proof,child_disproof = self.findtable(child_node)
            child_node.pn = child_proof
            child_node.dpn = child_disproof
            children.append(child_node)
        # iterative deepening, stop when TT max size is reached
        while node.pn>disproof_min(children) and node.dpn>proof_sum(children) and self.max_table_size>self.get_size() and not self.terminated:
            child,child_proof,child2_dpn = self.select_child(children)
            child.pn = node.dpn + child_proof - proof_sum(children)
            # e-trick
            if self.e:
                child.dpn = min(node.pn,child2_dpn*(1+self.e))
            else:
                child.dpn = min(node.pn,child2_dpn+1)
            # Second level search
            if self.second_level and (not self.in_table(child)):
                res,size = self.second_level(child)
                if child.node_type=="OR":
                    child.pn = res.pn
                    child.dpn = res.dpn
                else:
                    child.dpn = res.pn
                    child.pn = res.dpn
                self.putintable(child,size=size)
            else:
                self.expand(child)
        # store search result
        node.pn = disproof_min(children)
        node.dpn = proof_sum(children)
        self.putintable(node)

    
    def select_child(self,children):
        child_proof = float("inf")
        min_disproof = float("inf")
        value_set = False
        child2_dpn = float("inf")
        best = None
        for child in children:
            if not value_set or child.dpn < min_disproof:
                value_set = True
                best = child
                min_disproof,child2_dpn = child.dpn,min_disproof
                child_proof = child.pn
            elif child.dpn < child2_dpn:
                child2_dpn = child.dpn
            if child.pn == float("inf"):
                return best,child_proof,child2_dpn
        return best,child_proof,child2_dpn