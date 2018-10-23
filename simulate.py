from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import time

graph_complete = False
graph_complete_sequence = [False, False, False, False]


class Graph:
    def __init__(self, p_birth):
        self.p = p_birth
        self.q = 1 - self.p
        self.nodes = {
            1: [1],
            # 2: [1,4,3],
            # 3: [2,4],
            # 4: [2,3]
        }

        self.num_nodes_G = 0
        self.num_edges_G = 0
        self.update_num_nodes_and_edges()
        # self.run()

    def run(self):
        result = np.random.choice(['birth', 'death'], 1, p=[self.p, self.q])[0]
        # print result
        if result == 'birth':
            self.birth()
        elif result == 'death':
            self.death()

    def birth(self):
        preference_probability = []
        for node in self.nodes.keys():
            P_nodeU = len(self.nodes[node])/(2*self.num_edges_G)
            preference_probability.append(P_nodeU)

        preferred_node = np.random.choice(self.nodes.keys(), 1, p=preference_probability)[0]
        # new_node = int(self.nodes.keys()[-1]) + 1
        new_node = int(max(self.nodes.keys())) + 1


        # print "New node: ", new_node
        # print "preferred node to join: ", preferred_node
        self.update_nodes('birth', new_node, preferred_node)
        self.update_num_nodes_and_edges()
        # print("After Birth: \nGraph: {}".format(self.nodes))

    def death(self):
        preference_probability = []
        for node in self.nodes.keys():
            try:
                P_nodeU = (len(self.nodes) - len(self.nodes[node]))/ (len(self.nodes)**2 - 2*self.num_edges_G)
            except ZeroDivisionError as e:
                print("Graph Died")
                raise Exception('Exception raised in death()\nError: Attempted division by zero')

            preference_probability.append(P_nodeU)

        # print preference_probability
        # print self.nodes.keys()
        node_to_delete = np.random.choice(self.nodes.keys(), 1, p=preference_probability)[0]
        # print "Node to delete: ",node_to_delete
        self.update_nodes('death', node_to_delete)
        self.update_num_nodes_and_edges()
        # print("After death: \nGraph: {}".format(self.nodes))





    def update_num_nodes_and_edges(self):
        degree_G = 0
        for node in self.nodes:
            degree_G = degree_G + len(self.nodes[node])
        self.num_nodes_G = len(self.nodes)
        self.num_edges_G = degree_G/2                         # degree = 2*edges

    def update_nodes(self, mode, *args):
        if mode == 'birth':
            new_node = args[0]
            preferred_node = args[1]
            self.nodes[new_node] = [preferred_node]
            self.nodes[preferred_node].append(new_node)


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
                # if not self.nodes[node]:
                #     self.nodes.pop(node, None)

def main():
    global graph_complete
    global graph_complete_sequence

    start_time = time.time()
    number_of_iteration = 40000
    probabilities = [0.6, 0.75, 0.9, 0.8]
    graphs = []
    for p in probabilities:
        g = Graph(p)
        graphs.append(g)


    for key,graph in enumerate(graphs):
        #check if this current graph has been run previously, if yes don't run them again
        if not graph_complete_sequence[key]:
            x_time_step = []
            y_nodes = []
            y_edges = []
            for i in range(number_of_iteration):
                try:
                    graph.run()
                except ValueError as e:
                    print e
                    print "Graph Died: {}".format(graph.nodes)
                    print "Restarting Graph"
                    graph_complete = False
                    break
                except Exception as e:
                    print "Graph Died: {}".format(graph.nodes)
                    print "Restarting Graph"
                    # main()
                    graph_complete = False
                    break
                    # exit()
                x_time_step.append(i)
                y_nodes.append(graph.num_nodes_G)
                y_edges.append(graph.num_edges_G)


                graph_complete = True
                if (i+1) % 1000 == 0:
                    print "******TIME STEP {}******".format(i+1)
                    print "\n"

            if graph_complete == False:
                break

            # from itertools import groupby
            # frequency_of_degrees = [len(list(group)) for key, group in groupby(list_of_degree)]


            # insert a True value in the graph_complete_sequence_list, when we reach the end of graph
            graph_complete_sequence[key] = True
            graph_number = key + 1
            print "**************************************************"
            print "----------------END OF GRAPH {}-------------------".format(graph_number)
            print "**************************************************\n\n"


            if graph_number == 1 or graph_number == 2 or graph_number == 3:
                plt.subplot(2,2,1)
                plt.plot(x_time_step, y_nodes, label='p={}'.format(probabilities[key]))
                plt.xlabel('Time Step')
                plt.ylabel('Number of nodes')
                plt.title('Dynamic Graph')
                plt.legend()

                plt.subplot(2,2,2)
                plt.plot(x_time_step, y_edges, label='p={}'.format(probabilities[key]))
                plt.xlabel('Time Step')
                plt.ylabel('Number of Edges')
                plt.title('Dynamic Graph')
                plt.legend()

            # for graph 3, find cumulative distribution of degree of nodes
            if graph_number == 4:
                list_of_degree = [len(graph.nodes[key]) for key in graph.nodes.keys()]
                list_of_degree.sort()
                dict_degree_frequency = {x: list_of_degree.count(x) for x in list_of_degree}

                x_values = dict_degree_frequency.keys()
                frequencies = np.array(dict_degree_frequency.values())
                probabilities_x = frequencies / np.sum(frequencies)
                cumulative_probability_reverse = np.cumsum(probabilities_x[::-1])[::-1]

                plt.subplot(2, 2, 3)
                plt.plot(x_values, cumulative_probability_reverse,
                            label="p={}".format(probabilities[-1]),
                            marker='o',
                            linestyle='dotted')
                plt.xscale('log')
                plt.yscale('log')
                plt.xlabel('Degree')
                plt.ylabel('Cumulative Probability \n Distribution of degree')
                # plt.title('Dynamic Graph')
                plt.legend()


    if graph_complete:
        print "Total Time Taken: {}".format(time.time() - start_time)
        plt.show()


if __name__ == '__main__':
    while not graph_complete:
        main()

