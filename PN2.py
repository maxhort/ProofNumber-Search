from Tree import Node,Tree
from PN import PN
from constants import TRUE,FALSE,UNKNOWN
from math import e
class PN2:
    def __init__(self,name,root,evaluate_l2,
                result_l1,result_l2,get_pn_dpn_l1,get_pn_dpn_l2,max_nodes_l1,max_nodes_l2,
                delete_subtrees_l1=False,delete_subtrees_l2=False,immediateEvaluation_l1=False,immediateEvaluation_l2=True,
                a=50000,b=100000,max_evaluations=500000000):
        self.name = name
        self.evaluate_l2 = evaluate_l2
        self.result_l1 = result_l1
        self.result_l2 = result_l2
        self.get_pn_dpn_l1 = get_pn_dpn_l1
        self.get_pn_dpn_l2 = get_pn_dpn_l2
        self.max_nodes_l1 = max_nodes_l1
        self.max_nodes_l2 = max_nodes_l2
        self.delete_subtrees_l1 = delete_subtrees_l1
        self.delete_subtrees_l2 = delete_subtrees_l2
        self.immediateEvaluation_l1 = immediateEvaluation_l1
        self.immediateEvaluation_l2 = immediateEvaluation_l2
        self.root = root

        self.a = a
        self.b = b
        self.level1 = PN('level1',self.root,self.evaluate_level1,
                            self.result_l1,self.get_pn_dpn_l1,self.max_nodes_l1,self.delete_subtrees_l1,
                            self.immediateEvaluation_l1)
        self.level2 = PN('level2',self.root,self.evaluate_l2,self.result_l2,
                            self.get_pn_dpn_l2,self.max_nodes_l2,self.delete_subtrees_l2,self.immediateEvaluation_l2) 
        self.eval_count = 0
        self.max_evaluations = max_evaluations
    def evaluate_level1(self,node):
        self.level2.reset(Node(node.node_type,node.state,None,depth=0))
        self.set_level2_size()
        search_root = self.level2.perform_search()
        self.eval_count += self.level2.get_node_count()
        # If second level search came to result
        if search_root.pn == 0:
            node.value = TRUE
        elif search_root.dpn == 0:
            node.value = FALSE
        # Append children of second level search, if no definite result found
        else:
            node.value = UNKNOWN
            for child in search_root.children:
                child.parent = node
                self.level1.add_child(child,node)
            if search_root.children:
                node.expanded = True
        #del search_tree
        del search_root
        node.evaluated = True
        if self.eval_count>self.max_evaluations:
            self.level1.terminate()
    def reset(self,node):
        self.level1.reset(node)

    def set_level2_size(self):
        x = self.level1.get_size()
        self.level2.set_limit(min(self.max_nodes_l1-x,x+1))
        # logistic growth 
        # fraction = 1/(1+(a-x)/b)
        #self.level2.set_limit(min(self.max_nodes_l1-x,int(x*(1/(1+e**((self.a-x)/self.b))))))
    def perform_search(self):
        level1_result = self.level1.perform_search()
        return level1_result

    def set_evaluate(self,evaluate):
        self.level2.set_evaluate(evaluate)

    def get_size(self):
        return self.level1.get_size()

    def get_node_count(self):
        return self.eval_count