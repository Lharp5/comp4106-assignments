from node import Node
import random


class DependenceTree(object):
    def __init__(self, custom_define=False):
        self.nodes = []
        self.root = None
        if custom_define:
            self.root = Node('f0')
            self.nodes.append(self.root)
            f1 = self.root.create_child('f1')
            self.nodes.append(f1)
            f2 = self.root.create_child('f2')
            self.nodes.append(f2)
            f3 = self.root.create_child('f3')
            self.nodes.append(f3)
            f4 = f1.create_child('f4')
            self.nodes.append(f4)
            f5 = f1.create_child('f5')
            self.nodes.append(f5)
            f6 = f2.create_child('f6')
            self.nodes.append(f6)
            f7 = f2.create_child('f7')
            self.nodes.append(f7)
            f8 = f3.create_child('f9')
            self.nodes.append(f8)
            f9 = f3.create_child('f8')
            self.nodes.append(f9)

    def configure_from_mst(self, mst):
        mst_nodes = list(mst[0])
        mst_edges = list(mst[1])

        self.root = Node(mst_nodes[0])
        self.nodes.append(self.root)
        current_node = self.root
        nodes_left = []

        while current_node is not None:
            for e in list(mst_edges):
                other_node = None
                if e.start == current_node.id:
                    other_node = e.end
                elif e.end == current_node.id:
                    other_node = e.start

                # if we found an edge with our node,
                if other_node is not None:
                    # remove from our master copy
                    mst_edges.remove(e)
                    n = current_node.create_child(other_node)
                    self.nodes.append(n)

            # If we have more nodes to check for children iterate add in BFS manner
            if len(mst_nodes) > 0:
                nodes_left.extend(current_node.children)
                mst_nodes.remove(current_node.id)
                if len(nodes_left) == 0:
                    break
                current_node = nodes_left.pop()
            else:
                current_node = None

    def set_weights(self, weights):
        for node, weight in zip(self.nodes, weights):
            node.set_value(weight)

    def get_node(self, id):
        return next((x for x in self.nodes if x.id == id), None)

    def generate_weights(self, data):
        # Since our nodes were added in a BFS manner we can iterate through nodes and get weights
        for node in self.nodes:
            prob_given_parent = [0, 0]
            for x in range(2):  # determining based on parent value
                count = 0
                for d in data:  # iterating over all the data elements
                    if d.features[node.id] == 0:
                        # if we have no parent otherwise determine if parent value matches value we are looking for
                        if node.parent is None or d.features[node.parent.id] == x:
                            count += 1
                prob_given_parent[x] = float(count) / len(data)
            node.set_value(prob_given_parent)

    def __str__(self):
        output = ''
        for node in self.nodes:
            output += str(node) + ' :: Children '
            for child in node.children:
                output += str(child.id)
                output += ','
            output += '\n'

        return output

