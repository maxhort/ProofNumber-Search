from constants import TRUE,FALSE,UNKNOWN
class LayerSearch:
    def __init__(self,max_size):
        self.max_size = max_size
        self.layers = []

    def update_evaluation(self,i):
        self.layers[i].set_evaluate(lambda x: self.evaluate_layer(i,x))

    def add_layer(self,layer,layer_size = None):
        self.layers.append(layer)
        self.update_evaluation(len(self.layers)-1)


        # self.level2_pn = PN("pn",state,node_type,evaluate_pn,level2_result,set_pn,set_dpn,max_nodes,delete_subtrees=False,immediateEvaluation=True)
        # self.level1_pds = PDS("pds",state,node_type,evaluate_pds,result_pds,max_table_size_pds,second_level=self.second_level)
    def evaluate_layer(self,i,node):
        lower_layer = i+1
        self.layers[lower_layer].reset(node.state,node.node_type)
        #self.layers[lower_layer].set_limit()
        res = self.layers[lower_layer].perform_search()
        node.evaluated = True
        if res == 0:
            node.value = TRUE
        elif res.dpn == 0:
            node.value = FALSE
        else:
            node.value = UNKNOWN
        node.pn = res.pn
        node.dpn = res.dpn
    
    # def second_level(self,node):
    #     self.level2_pn.reset(node.state,node.node_type)
    #     x = self.level1_pds.TT.size()
    #     # logistic growth 
    #     # fraction = 1/(1+(a-x)/b)
    #     self.level2_pn.set_max_nodes(min(self.max_nodes-x,int(x*(1/(1+(self.a-x)/self.b)))))
    #     return self.level2_pn.perform_search()
    def perform_search(self):
        if self.layers:
            return self.layers[0].perform_search()
        