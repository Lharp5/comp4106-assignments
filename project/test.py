from generate_data import generate_data
from hand import Hand
from file_loader import load_data
from data import Data
from classifier import BayesianClassifier, DependenceTreeClassifier, DecisionTreeClassifier, print_matrix, calculate_accuracy
from dependence_tree import DependenceTree
from graph import Graph
from game import Game
from player import Player, AIPlayer


generate_data(80000)

# test_play = Hand('C9', ['C10', 'S10', 'HJ'], 'H10', 'C')
# result = test_play.is_valid()
# print test_play.to_binary()