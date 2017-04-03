import random

random.seed()


class Data(object):
    def __init__(self, num_features, dependency_tree=None, random_data=False):
        self.features = []
        for x in range(num_features):
            self.features.append(0)

        self.dependency_tree = dependency_tree
        if self.dependency_tree is not None and random_data:
            self.generate_random_data()

    def set_features(self, features):
        self.features = features

    def __str__(self):
        return str(self.features)

    def generate_random_data(self, new_tree=None):
        if new_tree is not None:
            self.dependency_tree = new_tree

        self.features = []
        for i, node in enumerate(self.dependency_tree.nodes):
            random_value = round(random.random(), 2)

            # root
            if node.parent is not None and i > 0 and self.features[i-1] == 1:
                weight = 1
            else:
                weight = 0

            self.features.append(0 if random_value <= node.value[weight] else 1)
