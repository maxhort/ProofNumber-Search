from PN import PN
from DFPN import DFPN
from DFPN_GHI import DFPN_GHI
from math import e
from Tree import Node
class DFPN_PN:
    def __init__(self,name,root,evaluate_dfpn,evaluate_pn,result_dfpn,level2_result,transposition_table,max_table_size_dfpn,
                max_nodes,get_pn_dpn_l1,get_pn_dpn_l2,a=50000,b=10000,e=None,max_evaluations=500000000):
        self.name = name
        self.max_nodes = max_nodes
        self.a = a
        self.b = b
        self.e = e
        self.level2_pn = PN("pn",root,evaluate_pn,level2_result,get_pn_dpn_l2,max_nodes,delete_subtrees=False,immediateEvaluation=True)
        self.level1_dfpn = DFPN_GHI("dfpn",root,evaluate_dfpn,result_dfpn,get_pn_dpn_l1,transposition_table,max_table_size_dfpn,e=self.e,second_level=self.second_level)
        
        self.eval_count = 0
        self.max_evaluations = max_evaluations
    def second_level(self,node):
        self.level2_pn.reset(Node(node.node_type,node.state,None,depth=0))
        x = self.level1_dfpn.TT.size()
        # logistic growth 
        # fraction = 1/(1+(a-x)/b)
        #self.level2_pn.set_limit(min(self.max_nodes-x,int(x*(1/(1+e**((self.a-x)/self.b))))))
        self.level2_pn.set_limit(min(self.max_nodes-x,x+1))
        res = self.level2_pn.perform_search()
        self.eval_count += self.level2_pn.get_node_count()
        if self.eval_count>self.max_evaluations:
            self.level1_dfpn.terminate()
        return res
    def reset(self,node):
        self.level1_dfpn.reset(node)
    def perform_search(self):
        return self.level1_dfpn.perform_search()

    def set_evaluate(self,evaluate):
        self.level2_pn.set_evaluate(evaluate)
        self.level1_dfpn.set_evaluate(evaluate)

    def get_size(self):
        return self.level1_dfpn.get_size()

    def get_node_count(self):
        return self.eval_count