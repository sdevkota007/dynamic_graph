from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, p_birth):
        self.p = p_birth
        self.q = 1 - self.p
        self.nodes = {
            1: [2],
            2: [1,4,3],
            3: [2,4],
            4: [2,3]
        }
        # self.nodes = {
        #     "1": ['3'],
        #     "2": ['3'],
        #     '3': ['1','2']
        # }
        self.num_edges_G = 0
        self.update_num_edges()
        #self.run()

    def run(self):
        result = np.random.choice(['birth', 'death'], 1, p=[self.p, self.q])[0]
        print result
        if result == 'birth':
            self.birth()
        elif result == 'death':
            self.death()

    def birth(self):
        preference_probability = []
        for node in self.nodes.keys():
            P_nodeU = len(self.nodes[node])/(2*self.num_edges_G)
            preference_probability.append(P_nodeU)

        print preference_probability
        print self.nodes.keys()
        preferred_node = np.random.choice(self.nodes.keys(), 1, p=preference_probability)[0]
        #new_node = int(self.nodes.keys()[-1]) + 1
        new_node = int(max(self.nodes.keys())) + 1


        print "New node: ", new_node
        print "preferred node to join: ", preferred_node
        self.update_nodes('birth', new_node, preferred_node)
        self.update_num_edges()


    def death(self):
        preference_probability = []
        for node in self.nodes.keys():
            P_nodeU = (len(self.nodes) - len(self.nodes[node]))/ (len(self.nodes)**2 - 2*self.num_edges_G)
            preference_probability.append(P_nodeU)
        print preference_probability
        print self.nodes.keys()
        node_to_delete = np.random.choice(self.nodes.keys(), 1, p=preference_probability)[0]
        print "Node to delete: ",node_to_delete
        self.update_nodes('death', node_to_delete)
        self.update_num_edges()


    def update_num_edges(self):
        degree_G = 0
        for node in self.nodes:
            degree_G = degree_G + len(self.nodes[node])
        self.num_edges_G = degree_G/2                         # degree = 2*edges

    def update_nodes(self, mode, *args):
        if mode == 'birth':
            new_node = args[0]
            preferred_node = args[1]
            self.nodes[new_node] = [preferred_node]
            self.nodes[preferred_node].append(new_node)
            print self.nodes


        elif mode == 'death':
            node_to_delete = args[0]
            #delete the selected node from the graph
            self.nodes.pop(node_to_delete, None)
            for node in self.nodes.keys():
                #delete the edge from all the other nodes that was connected to the deleted node
                if node_to_delete in self.nodes[node]:
                    self.nodes[node].remove(node_to_delete)

                # check if the node from which we deleted an edge has no edges left,
                # in that case delete that node, which is hanging without an edge
                if not self.nodes[node]:
                    self.nodes.pop(node, None)

            print self.nodes


if __name__ == '__main__':
    number_of_iteration = 1000
    g = Graph(0.7)
    for i in range(number_of_iteration):
        print "*****************TIME STEP {}********************".format(i)
        g.run()
        print "\n \n"

    x = [1, 2, 3]
    y = [5, 7, 4]

    x2 = [1, 2, 3]
    y2 = [10, 14, 12]


    plt.plot(x, y, label='First Line')
    #plt.plot(x2, y2, label='Second Line')