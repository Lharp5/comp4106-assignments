from data import Data
from copy import deepcopy
from node import Node
import math
import itertools


def print_matrix(mat):
    print(''.join(['{:9} '.format('Class '+str(row+1)) for row in range(len(mat[0]))]))
    print('\n'.join([''.join(['{:8} '.format(round(item, 2)) for item in row]) for row in mat]))


def calculate_accuracy(acc):
    count = 0
    tally = 0.0

    for row in acc:
        for item in row:
            count += 1
            tally += item

    return tally / count


class Class(object):
    # Default 5-fold validation
    def __init__(self, data, fold_validation):
        self.fold = fold_validation
        self.class_data = data
        self.testing_size = len(self.class_data) / fold_validation

    def get_testing_data(self, chunk):
        return self.class_data[self.testing_size*chunk:self.testing_size * (chunk + 1)]

    def get_training_data(self, testing_chunk):
        # Check if we are testing the first chunk, take everything after testing data
        if testing_chunk == 0:
            return self.class_data[self.testing_size * (testing_chunk + 1):]

        # If we are getting the last chunk take everything before testing data
        if testing_chunk == 4:
            return self.class_data[: self.testing_size * testing_chunk]

        # return the training data with the testing data removed
        return self.class_data[: self.testing_size * testing_chunk] + \
               self.class_data[self.testing_size * (testing_chunk + 1):]


class Classifier(object):
    def __init__(self, class_data, num_features, fold_validation=5):
        self.classes = []
        self.num_features = num_features
        self.fold_validation = fold_validation
        for data in class_data:
            self.classes.append(Class(data, self.fold_validation))

        self.confusion_matrix = []
        for x in range(len(self.classes)):
            self.confusion_matrix.append([])
            for y in range(len(self.classes)):
                self.confusion_matrix[x].append(0)

    # returns the accuracy
    def train(self):
        class_testing_data = []
        class_training_data = []
        accuracy = []
        for i in range(self.fold_validation):
            print "\nIteration: "+str(i)
            class_testing_data.append([])
            class_training_data.append([])

            # Split our data in to training and testing
            for a_class in self.classes:
                class_testing_data[i].append(a_class.get_testing_data(i))
                class_training_data[i].append(a_class.get_training_data(i))

            # train our data using Bayes by
            accuracy.append(self.perform_train_and_test(class_training_data[i], class_testing_data[i]))
            for x in range(len(self.confusion_matrix)):
                for y in range(len(self.confusion_matrix[x])):
                    self.confusion_matrix[x][y]= float(self.confusion_matrix[x][y]) / len(class_testing_data[i][y])
            print "Confusion Matrix"
            print_matrix(self.confusion_matrix)

            for x in range(len(self.confusion_matrix)):
                for y in range(len(self.confusion_matrix[x])):
                    self.confusion_matrix[x][y] = 0

        return accuracy

    # Override this method. Returns the accuracy
    def perform_train_and_test(self, training_data, testing_data):
        return 0

    def evaluate(self, data):
        pass


class BayesianClassifier(Classifier):
    def __init__(self, class_data, num_features):
        Classifier.__init__(self, class_data, num_features)
        self.class_probabilities = []
        for x in range(0, len(self.classes)):
            self.class_probabilities.append(Data(self.num_features))

    def perform_train_and_test(self, training_data, testing_data):

        # Reset our trained data
        for x in range(len(self.class_probabilities)):
            self.class_probabilities[x] = Data(self.num_features)

        for i, class_training_data in enumerate(training_data):
            for data in class_training_data:
                for j in range(len(data.features)):
                    # Add if we found a 0 otherwise we found a 1
                    self.class_probabilities[i].features[j] += 1 if data.features[j] == 0 else 0

        # now that we have the total number of instances found in each, turn them into probabilities
        for probability in self.class_probabilities:
            for n in range(len(probability.features)):
                probability.features[n] = float(probability.features[n]) / len(training_data[0])

        # Test each class
        class_accuracy = []

        for c, class_testing_data in enumerate(testing_data):
            class_accuracy.append(0)
            for data in class_testing_data:
                best_guess, best_confidence = self.evaluate(data)
                self.confusion_matrix[c][best_guess] += 1

                if best_guess == c:
                    class_accuracy[c] += 1

            # Changing the confidence from a count to a probability of how many classes it should have correctly guessed
            class_accuracy[c] = float(class_accuracy[c]) / len(class_testing_data)
            print "Class "+str(c) + " Accuracy: "+str(class_accuracy[c])

        return class_accuracy

    def evaluate(self, data):
        best_guess = -1
        best_confidence = -1

        for bc, probability in enumerate(self.class_probabilities):
            confidence = 1.0
            for feature, prob in zip(data.features, probability.features):
                confidence *= prob if feature == 0 else (1.0 - prob)

            if confidence > best_confidence:
                best_confidence = confidence
                best_guess = bc

        return best_guess, best_confidence


class DependenceTreeClassifier(Classifier):
    def __init__(self, class_data, num_features, dep_trees):
        self.depTrees = dep_trees
        Classifier.__init__(self, class_data, num_features)

    def perform_train_and_test(self, training_data, testing_data):

        # Training our tree
        for data, tree in zip(training_data, self.depTrees):
            # Calculate edge weights of the tree for each data point
            tree.generate_weights(data)
            # print "Class Generated Weights"
            # print tree

        # Test each class
        class_accuracy = []
        for c, class_testing_data in enumerate(testing_data):
            class_accuracy.append(0)

            # for each data in the class
            for data in class_testing_data:
                best_guess, best_confidence = self.evaluate(data)
                self.confusion_matrix[c][best_guess] += 1

                if best_guess == c:
                    class_accuracy[c] += 1

            # Changing the confidence from a count to a probability of how many classes it should have correctly guessed
            class_accuracy[c] = float(class_accuracy[c]) / len(class_testing_data)
            print "Class " + str(c) + " Accuracy: " + str(class_accuracy[c])

        return class_accuracy

    def evaluate(self, data):
        best_guess = -1
        best_confidence = -1

        for tc, tree in enumerate(self.depTrees):
            confidence = 1.0
            for f, feature in enumerate(data.features):
                n = tree.get_node(f)

                # Check for root
                if n.parent is None:
                    confidence *= n.value[0] if feature == 0 else (1 - n.value[0])
                else:  # Check the parent's value, and get the probability of the current feature
                    confidence *= n.value[data.features[n.parent.id]] if \
                        feature == 0 else (1 - n.value[data.features[n.parent.id]])

            if confidence > best_confidence:
                best_confidence = confidence
                best_guess = tc

        return best_guess, best_confidence


def entropy(pair):
    total_size = sum(pair)
    if total_size == float(0) or (float(pair[0])/total_size) == float(0) or (float(pair[1])/total_size) == float(0):
        return 0
    return -(float(pair[0])/total_size) * math.log((float(pair[0])/total_size), 2) \
           - (float(pair[1])/total_size) * math.log((float(pair[1])/total_size), 2)


class DecisionTreeClassifier(Classifier):
    def __init__(self, class_data, num_features):
        self.root_dict = {}
        Classifier.__init__(self, class_data, num_features)

    def generate_tree(self, positive_set, negative_set, parent_node=None, nodes=None):
        # Determine what value to set
        def base_case(num_pos, num_neg):
            if num_pos >= num_neg:
                parent_node.set_value(0)
            else:
                parent_node.set_value(1)
            return None
        # Check Base Case that we have every node in the list
        if nodes is not None and len(nodes) == self.num_features:
            return base_case(len(positive_set), len(negative_set))

        new_positive_0_set = []
        new_negative_0_set = []
        new_positive_1_set = []
        new_negative_1_set = []
        best_gain = -1
        best_feature = -1
        root = None
        current_node = None

        current_node_list = []

        # add the list we passed in
        if nodes is not None:
            current_node_list.extend(nodes)

        for i in range(self.num_features):
            # If we are iterating to a node that is already in our list skip,
            if parent_node is not None and any(x.id == i for x in nodes):
                continue
            curr_pos_0_set = []
            curr_neg_0_set = []
            curr_pos_1_set = []
            curr_neg_1_set = []

            # Getting all the occurances in a positive set
            for positive in positive_set:
                if positive.features[i] == 0:
                    curr_pos_0_set.append(positive)
                else:
                    curr_pos_1_set.append(positive)

            # Getting all the occurances in a negative set
            for negative in negative_set:
                if negative.features[i] == 0:
                    curr_neg_0_set.append(negative)
                else:
                    curr_neg_1_set.append(negative)

            # Information Gain Calculations
            s0 = [len(curr_pos_0_set), len(curr_neg_0_set)]
            s1 = [len(positive_set) - len(curr_pos_0_set), len(negative_set) - len(curr_neg_0_set)]

            s = [s0[0] + s1[0], s0[1] + s1[1]]

            # Base case #2
            if entropy(s) == 0:
                return base_case(s[0], s[1])

            total_data = len(positive_set) + len(negative_set)
            gain = entropy(s) - (float(sum(s0)) / total_data)*entropy(s0) - (float(sum(s1)) / total_data)*entropy(s1)

            if gain > best_gain:
                best_gain = gain
                best_feature = i
                new_positive_0_set = curr_pos_0_set
                new_negative_0_set = curr_neg_0_set
                new_positive_1_set = curr_pos_1_set
                new_negative_1_set = curr_neg_1_set

        # Create new node on the best gain
        if parent_node is None:
            root = Node(best_feature)
            current_node = root
        else:
            current_node = parent_node.create_child(best_feature)

        # add our node to the current node list
        current_node_list.append(current_node)

        # Recursively create tree from 0 and 1.
        self.generate_tree(new_positive_0_set, new_negative_0_set, current_node, current_node_list)
        self.generate_tree(new_positive_1_set, new_negative_1_set, current_node, current_node_list)
        return root

    def perform_train_and_test(self, training_data, testing_data):
        # Test each class

        self.root_dict = {}

        # Training, generate all the combinations of decision trees for the training data
        for a, b in itertools.combinations(training_data, 2):
            self.root_dict[(training_data.index(a), training_data.index(b))] = self.generate_tree(a, b)

        class_accuracy = []
        for c, test_data in enumerate(testing_data):
            class_accuracy.append(0)
            # Using pairwise classification
            for data in test_data:
                best_guess, best_confidence = self.evaluate(data)
                self.confusion_matrix[c][best_guess] += 1

                # Determine success or failure of classification
                if best_guess == c:
                    class_accuracy[c] += 1

            # Changing the confidence from a count to a probability of how many classes it should have correctly guessed
            class_accuracy[c] = float(class_accuracy[c]) / len(test_data)
            print "Class " + str(c) + " Accuracy: " + str(class_accuracy[c])

        return class_accuracy

    def evaluate(self, data):
        best_guess = 0
        for next_class in range(1, len(self.classes)):
            current_node = self.root_dict.get((best_guess, next_class), None)
            while current_node is not None:
                # If we have a value, we found the leaf, check to see which class it wishes to classify
                if current_node.value is not None:
                    if current_node.value == 1:
                        best_guess = next_class
                    break

                # Progress through tree
                decision = data.features[current_node.id]
                current_node = current_node.children[decision]

        return best_guess, -1

        pass
