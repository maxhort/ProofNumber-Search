from PN import PN
from PDS import PDS
from PDS_GHI import PDS_GHI
from Tree import Node
from math import e
class PDS_PN:
    def __init__(self,name,root,evaluate_pds,evaluate_pn,result_pds,level2_result,transposition_table,max_table_size_pds,
                max_nodes,get_pn_dpn_l1,get_pn_dpn_l2,a=50000,b=10000,e=None,max_evaluations=500000000):
        self.name = name
        self.max_nodes = max_nodes
        self.a = a
        self.b = b
        self.e = e

        self.level2_pn = PN("pn",root,evaluate_pn,level2_result,get_pn_dpn_l2,max_nodes,delete_subtrees=False,immediateEvaluation=True)
        self.level1_pds = PDS_GHI("pds",root,evaluate_pds,result_pds,get_pn_dpn_l1,transposition_table,max_table_size_pds,e=self.e,second_level=self.second_level)
        self.eval_count = 0
        self.max_evaluations = max_evaluations
    def second_level(self,node):
        self.level2_pn.reset(Node(node.node_type,node.state,None,depth=0))
        x = self.level1_pds.TT.size()
        # logistic growth 
        # fraction = 1/(1+(a-x)/b)
        self.level2_pn.set_limit(min(self.max_nodes-x,x+1))
        #self.level2_pn.set_limit(min(self.max_nodes-x,int(x*(1/(1+e**((self.a-x)/self.b))))))
        res = self.level2_pn.perform_search()
        self.eval_count += self.level2_pn.get_node_count()
        if self.eval_count>self.max_evaluations:
            self.level1_pds.terminate()
        return res
    def reset(self,node):
        self.level1_pds.reset(node)
    def perform_search(self):
        return self.level1_pds.perform_search()

    def set_evaluate(self,evaluate):
        self.level2_pn.set_evaluate(evaluate)
        self.level1_pds.set_evaluate(evaluate)

    def get_size(self):
        return self.level1_pds.get_size()

    def get_node_count(self):
        return self.eval_count