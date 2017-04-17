from dependence_tree import DependenceTree
from data import Data
from classifier import BayesianClassifier, DependenceTreeClassifier, print_matrix, calculate_accuracy, DecisionTreeClassifier
from graph import Graph
from file_loader import Load_File_Data


real_data_file = 'wine.csv'
real_data, real_num_features = Load_File_Data(real_data_file)

for i in range(len(real_data)):
    real_data[i] = [Data(real_num_features, data=feature_list) for feature_list in real_data[i]]

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

generated_class_data = [[], [], [], []]

for i in range(2000):
    generated_class_data[0].append(Data(10, c1dt, True))
    generated_class_data[1].append(Data(10, c2dt, True))
    generated_class_data[2].append(Data(10, c3dt, True))
    generated_class_data[3].append(Data(10, c4dt, True))

var = raw_input("Real World Data (1) or Generated Data (2) : ")
if int(var) == 1:
    print "Using Real World Data"
    class_data = real_data
    num_features = real_num_features
else:
    print "Using Generated Data"
    class_data = generated_class_data
    num_features = 10

depTrees = list()
for x in range(len(class_data)):
    depTrees.append(DependenceTree())

g = Graph(num_features, class_data)
mst = g.run_max_prim()

for tree in depTrees:
    tree.configure_from_mst(mst)

print "Independent Bayesian Classifier: Accuracy By Run:"
bc = BayesianClassifier(class_data, num_features)
accuracy = bc.train()
print "Indep Bayes Accuracy Per Fold:"
print_matrix(accuracy)
2
print "Dependency Tree Classifier: Accuracy By Run:"
depc = DependenceTreeClassifier(class_data, num_features, depTrees)
depAccuracy = depc.train()
print "DepTree Accuracy Per Fold:"
print_matrix(depAccuracy)

print "Decision Tree Classifier:"
decc = DecisionTreeClassifier(class_data, num_features)
decAccuracy = decc.train()

print "DecTree Accuracy Per Fold:"
print_matrix(decAccuracy)

print "Independent Bayesian Accuracy: " + str(calculate_accuracy(accuracy))
print "Dependency Tree Accuracy: " + str(calculate_accuracy(depAccuracy))
print "Decision Tree Accuracy: " + str(calculate_accuracy(decAccuracy))

