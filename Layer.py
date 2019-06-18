class Layer:
    def __init__(self, search, process_result = lambda search,node,result: None, calculate_max_size = lambda x:50000):
        self.search = search
        self.process_result = process_result
        self.calculate_max_size = calculate_max_size
        
    def reset(self, node, upper_layer_size):
        self.search.reset(node.state,node.node_type)
        self.search.set_limit(self.calculate_max_size(upper_layer_size))
    
    def get_size(self):
        return self.search.get_size()
    
    def update_second_level(self,evaluate):
        self.search.set_second_level(evaluate)
        
    def perform_search(self):
        return self.search.perform_search()
        
class LayerSearch:
    def __init__(self,max_size):
        self.max_size = max_size
        self.layers = []

    def update_second_level(self,i):
        self.layers[i].update_second_level(lambda x: self.evaluate_layer(i,x))

    def add_layer(self,layer,layer_size = None):
        self.layers.append(layer)
        if len(self.layers)>1:
            self.update_second_level(len(self.layers)-2)

    def evaluate_layer(self,i,node):
        lower_layer = i+1
        self.layers[lower_layer].reset(node,self.layers[i].get_size())
        res = self.layers[lower_layer].perform_search()
        self.layers[i].process_result(self.layers[i].search,node,res)
        return res
    
    def perform_search(self):
        if self.layers:
            return self.layers[0].perform_search()
        