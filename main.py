# Mishukov Konstantin
# 2021

import getopt
import sys
import re
from myQueue import Queue

import numpy as np

# main.py -i m.txt

path = ''
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["ifile="])
except getopt.GetoptError:
    print('main.py -i <inputfile>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('main.py -i <inputfile>')
        sys.exit()
    elif opt in ("-i", "--ifile"):
        path = arg

if path == "":
    print('Missing parameters.')
    print('main.py -i <inputfile>')
    sys.exit(2)


def parsefile(filepath):
    try:
        mtx = np.loadtxt(filepath, dtype='int')
        print('Input Matrix:\n', mtx)
        return mtx
    except IOError:
        print("Error: file could not be opened")
        sys.exit(2)


matrix = parsefile(path)
matrix_size: int = len(matrix)

maxsize = float('inf')
best_solution_record = float('inf')
best_solution = None
solutions_queue = Queue()


# Calculate lower bound on any given solution (step);
def calculate_bound(solution) -> float:
    summary = 0
    for i in range(matrix_size):
        first_minimum = float('inf')
        second_minimum = float('inf')
        for j in range(matrix_size):
            current_branch = Branch(i, j)
            if i == j or solution.branches[current_branch] is False:
                continue
            if matrix[i][j] <= first_minimum:
                second_minimum = first_minimum
                first_minimum = matrix[i][j]
            elif matrix[i][j] < second_minimum:
                second_minimum = matrix[i][j]
        summary += first_minimum + second_minimum
    return summary * 0.5


def make_branches(solution):
    global best_solution_record
    global best_solution
    if solution.number_of_included_branches() >= matrix_size - 2:
        include_branches_if_needed(solution)
        solution_total_bound = solution.current_bound()
        print("Record achieved:", solution_total_bound)
        if solution_total_bound < best_solution_record:
            best_solution_record = solution.current_bound()
            best_solution = solution
        return
    for i in range(matrix_size):
        if solution.has_two_adjacents_to_node(i):
            continue
        for j in range(matrix_size):
            if i == j:
                continue
            current_branch = Branch(i, j)
            if current_branch in solution.branches.keys():
                continue

            new_solution1 = Solution()
            new_solution1.branches = solution.branches.copy()
            new_solution1.branches[current_branch] = True
            if new_solution1.has_two_adjacents_to_node(i):
                exclude_possible_short_circuit_at(new_solution1, j)
            exclude_branches_for_filled_nodes(new_solution1)

            new_solution2 = Solution()
            new_solution2.branches = solution.branches.copy()
            new_solution2.branches[current_branch] = False
            include_branches_if_needed(new_solution2)

            if new_solution1.current_bound() <= best_solution_record:
                solutions_queue.enqueue(new_solution1)
            if new_solution2.current_bound() <= best_solution_record:
                solutions_queue.enqueue(new_solution2)
            return


class Branch:
    def __init__(self, node_a, node_b):
        if node_a > node_b:
            self.nodeA = node_b
            self.nodeB = node_a
        else:
            self.nodeA = node_a
            self.nodeB = node_b

    def __eq__(self, other):
        if isinstance(other, Branch):
            return (self.nodeA == other.nodeA and self.nodeB == other.nodeB) or (
                        self.nodeA == other.nodeB and self.nodeB == other.nodeA)
        return False

    def __hash__(self):
        if self.nodeA < self.nodeB:
            return hash((self.nodeA, self.nodeB))
        else:
            return hash((self.nodeB, self.nodeA))

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return '(' + str(self.nodeA) + ', ' + str(self.nodeB) + ')'

    def is_incident_to(self, node):
        return self.nodeA == node or self.nodeB == node


class Solution:
    def __init__(self):
        self.branches = dict()
        self.nodes = dict()
        self.path = []

    def current_bound(self):
        summary = 0
        for i in range(matrix_size):
            first_minimum = float('inf')
            second_minimum = float('inf')
            for j in range(matrix_size):
                current_branch = Branch(i, j)
                if i == j or self.branches.get(current_branch) is False:
                    continue
                if matrix[i][j] <= first_minimum:
                    second_minimum = first_minimum
                    first_minimum = matrix[i][j]
                elif matrix[i][j] < second_minimum:
                    second_minimum = matrix[i][j]
            summary += first_minimum + second_minimum
        return summary * 0.5

    def has_two_adjacents_to_node(self, node):
        adjacents_counter = 0
        for branch in self.branches.keys():
            if branch.is_incident_to(node) and self.branches[branch] is True:
                adjacents_counter += 1
                if adjacents_counter == 2:
                    return True
        return False

    def number_of_included_branches(self):
        number = 0
        for k in self.branches.keys():
            if self.branches[k] is True:
                number += 1
        return number

    def print_solution(self):
        if self.number_of_included_branches() != matrix_size:
            print('Error: tried printing not complete solution.')
            return
        path = '0'
        zero_branches = []
        true_branches = []
        for branch in self.branches.keys():
            if self.branches[branch] is True:
                true_branches.append(branch)
        for branch in true_branches:
            if branch.is_incident_to(0):
                zero_branches.append(branch)
        current_branch = (zero_branches[0], zero_branches[1])[zero_branches[0].nodeA < zero_branches[1].nodeB]
        current_node = current_branch.nodeB
        while current_node != 0:
            path += str(current_node)
            for branch in true_branches:
                if branch.is_incident_to(current_node) and branch != current_branch:
                    current_node = (branch.nodeA, branch.nodeB)[branch.nodeA == current_node]
                    current_branch = branch
                    break
        path += '0'
        print("Solution Path:", path)


def exclude_branches_for_filled_nodes(solution):
    for i in range(matrix_size):
        if solution.has_two_adjacents_to_node(i):
            for j in range(matrix_size):
                if i == j:
                    continue
                branch_to_exclude = Branch(i, j)
                if branch_to_exclude not in solution.branches.keys():
                    solution.branches[branch_to_exclude] = False


def include_branches_if_needed(solution):
    for i in range(matrix_size):
        number_of_excluded_branches = 0
        for b in solution.branches.keys():
            if b.is_incident_to(i) and solution.branches[b] is False:
                number_of_excluded_branches += 1
        if number_of_excluded_branches > matrix_size - 3:
            print("Error in number of excluded branches on node: ", i)
            sys.exit(2)
        if number_of_excluded_branches == matrix_size - 3:
            for j in range(matrix_size):
                if i == j:
                    continue
                current_branch = Branch(i, j)
                if current_branch not in solution.branches.keys():
                    solution.branches[current_branch] = True
                    if solution.has_two_adjacents_to_node(i):
                        exclude_possible_short_circuit_at(solution, j)


def exclude_possible_short_circuit_at(solution, j):
    if solution.number_of_included_branches() == matrix_size - 1:
        return
    for i in range(matrix_size):
        if i == j:
            continue
        branch_to_exclude = Branch(i, j)
        if branch_to_exclude in solution.branches.keys():
            continue
        if has_included_adjacents(solution, branch_to_exclude):
            solution.branches[branch_to_exclude] = False
            return


def has_included_adjacents(solution, branch) -> bool:
    node_a_included = False
    node_b_included = False
    included_branches = []
    for b in solution.branches.keys():
        if solution.branches[b] is True:
            included_branches.append(b)
    for b in included_branches:
        if b.is_incident_to(branch.nodeA):
            node_a_included = True
            continue
        if b.is_incident_to(branch.nodeB):
            node_b_included = True
    return node_a_included and node_b_included


def are_incident(branch1: Branch, branch2: Branch) -> bool:
    return branch1.nodeA == branch2.nodeA or branch1.nodeA == branch2.nodeB or\
           branch1.nodeB == branch2.nodeA or branch1.nodeB == branch2.nodeB


if __name__ == '__main__':
    initial_solution = Solution()
    solutions_queue.enqueue(initial_solution)
    counter = 0
    while solutions_queue.size() > 0:
        current_solution = solutions_queue.dequeue()
        if counter == 0:
            print('Lower bound at start is:', current_solution.current_bound())
        else:
            print('Current step:', counter, ', current_bound:', current_solution.current_bound())
        make_branches(current_solution)
        counter += 1
    print('\nAlgorithm finished')
    print('Best solution is: ', best_solution_record)
    best_solution.print_solution()
