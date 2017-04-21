from generate_data import generate_data
from hand import Hand
from file_loader import load_data
from data import Data
from classifier import BayesianClassifier, DependenceTreeClassifier, DecisionTreeClassifier, print_matrix, calculate_accuracy
from dependence_tree import DependenceTree
from graph import Graph
from game import Game
from player import Player, AIPlayer

valid_lines, invalid_lines, num_features = load_data('correct_move.txt', 'incorrect_move.txt')


valid_data = [Data(num_features, data=valid_play) for valid_play in valid_lines]
invalid_data = [Data(num_features, data=invalid_play) for invalid_play in invalid_lines]

class_data = [valid_data, invalid_data]

print "Data Loading Complete"

# Bayesian independent

print "Independent Bayesian Classifier: Accuracy By Run:"
bc = BayesianClassifier(class_data, num_features)
accuracy = bc.train()
print "Indep Bayes Accuracy Per Fold:"
print_matrix(accuracy)

# Dependence Trees Classifier

depTrees = list()
for x in range(len(class_data)):
    depTrees.append(DependenceTree())

print "Building Dependence Tree Graph...."
g = Graph(num_features, class_data)
mst = g.run_max_prim()

for tree in depTrees:
    tree.configure_from_mst(mst)

print "Dependency Tree Classifier: Accuracy By Run:"
depc = DependenceTreeClassifier(class_data, num_features, depTrees)
depAccuracy = depc.train()
print "DepTree Accuracy Per Fold:"
print_matrix(depAccuracy)

# Decision Tree Classifier

print "Decision Tree Classifier:"
decc = DecisionTreeClassifier(class_data, num_features)
decAccuracy = decc.train()

print "DecTree Accuracy Per Fold:"
print_matrix(decAccuracy)

print "Independent Bayesian Accuracy: " + str(calculate_accuracy(accuracy))
print "Dependency Tree Accuracy: " + str(calculate_accuracy(depAccuracy))
print "Decision Tree Accuracy: " + str(calculate_accuracy(decAccuracy))


players = [Player('Player'), AIPlayer('Computer1', bc), AIPlayer('Computer2', depc), AIPlayer('Computer3', decc)]
game = Game(players)
game.setup()
game.run()
game.end()
