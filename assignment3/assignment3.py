from dependence_tree import DependenceTree
from data import Data
from classifier import BayesianClassifier, DependenceTreeClassifier, print_matrix, calculate_accuracy, DecisionTreeClassifier
from graph import Graph

c1dt = DependenceTree(True)
c2dt = DependenceTree(True)
c3dt = DependenceTree(True)
c4dt = DependenceTree(True)

c1dt.set_weights([[0.89, 0.89], [0.88, 0.87], [0.55, 0.68], [0.04, 0.23], [0.25, 0.59], [0.85, 0.68], [0.1, 0.09], [0.87, 0.0], [0.49, 0.86], [0.83, 0.43]])
c2dt.set_weights([[0.8, 0.8], [0.83, 0.41], [0.91, 0.57], [0.4, 0.28], [0.52, 0.15], [0.03, 0.21], [0.72, 0.37], [0.25, 0.64], [0.6, 0.17], [0.27, 0.16]])
c3dt.set_weights([[0.89, 0.89], [0.68, 0.57], [0.13, 0.05], [0.6, 0.42], [0.18, 0.06], [0.7, 0.15], [0.31, 0.01], [0.86, 0.46], [0.23, 0.93], [0.65, 0.51]])
c4dt.set_weights([[0.23, 0.23], [0.69, 0.21], [0.96, 0.68], [0.44, 0.89], [0.69, 0.68], [0.27, 0.07], [0.55, 0.06], [0.55, 0.99], [0.74, 0.26], [0.15, 0.41]])

print "Class 1 Generated DepTree"
print c1dt
print "Class 2 Generated DepTree"
print c2dt
print "Class 3 Generated DepTree"
print c3dt
print "Class 4 Generated DepTree"
print c4dt

class_data = [[], [], [], []]

for i in range(2000):
    class_data[0].append(Data(10, c1dt, True))
    class_data[1].append(Data(10, c2dt, True))
    class_data[2].append(Data(10, c3dt, True))
    class_data[3].append(Data(10, c4dt, True))

depTrees = list()
depTrees.append(DependenceTree())
depTrees.append(DependenceTree())
depTrees.append(DependenceTree())
depTrees.append(DependenceTree())

g = Graph(10, class_data)
mst = g.run_max_prim()
depTrees[0].configure_from_mst(mst)
depTrees[1].configure_from_mst(mst)
depTrees[2].configure_from_mst(mst)
depTrees[3].configure_from_mst(mst)

print "Independent Bayesian Classifier: Accuracy By Run:"
bc = BayesianClassifier(class_data, 10)
accuracy = bc.train()
print_matrix(accuracy)

print "Independent Bayesian Accuracy: " + str(calculate_accuracy(accuracy))

print "Dependency Tree Classifier: Accuracy By Run:"
depc = DependenceTreeClassifier(class_data, 10, depTrees)
depAccuracy = depc.train()
print_matrix(depAccuracy)

print "Dependency Tree Accuracy: " + str(calculate_accuracy(depAccuracy))

print "Decision Tree Classifier: Accuracy By Run:"
decc = DecisionTreeClassifier(class_data, 10)
decAccuracy = decc.train()
print_matrix(decAccuracy)

print "Dependency Tree Accuracy: " + str(calculate_accuracy(decAccuracy))

