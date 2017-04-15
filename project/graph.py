from edge import Edge
import itertools
import math


class Graph(object):
    def __init__(self, numberOfVertices, data):
        self.vertices = []
        self.edges = []
        for x in range(numberOfVertices):
            self.vertices.append(x)

        flat_data = []
        for entry in data:
            flat_data += entry

        # Generate our edges using Expected Mutual information Measure
        for x, y in itertools.combinations(self.vertices, 2):
            emi = 0
            for i, j in itertools.permutations([0, 1]):
                cij = 0
                ci = 0
                cj = 0
                for data in flat_data:
                    if data.features[x] == i and data.features[y] == j:
                        cij += 1

                    if data.features[x] == i:
                        ci += 1

                    if data.features[y] == j:
                        cj += 1

                pij = float(cij) / len(flat_data)
                pi = float(ci) / len(flat_data)
                pj = float(cj) / len(flat_data)
                test = pij / (pi * pj)
                emi += pij * math.log(test, 2)

            self.edges.append(Edge(x, y, emi))

    def run_max_prim(self):

        mst_edges = []
        mst_vertices = set()

        current_vertex = self.vertices[0]
        mst_vertices.add(current_vertex)
        edges_left = list(self.edges)
        edges_left.sort(key=lambda x: x.weight, reverse=True)

        for edge in edges_left:
            # From highest weighted edge down check to see if only one end is in the list
            if edge.start in mst_vertices and edge.end not in mst_vertices:
                mst_vertices.add(edge.end)

            elif edge.start not in mst_vertices and edge.end in mst_vertices:
                mst_vertices.add(edge.start)

            else:  # If neither are in, or both are in skip this edge
                continue

            # If we have found 1 end of the edge not in the MST we add to the MST and record the edge
            mst_edges.append(edge)

            # If we have added all vertices to the MST, no point in continuing
            if len(mst_vertices) >= len(self.vertices):
                break

        return list(mst_vertices), mst_edges
