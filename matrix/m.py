import numpy as np
import getopt
import sys
import enum
import random

class Mode(enum.Enum):
   Test = 1
   Create = 2
   Unknown = 3

current_mode = Mode.Unknown
path = ''
size = 0
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:c:", ["ifile="])
except getopt.GetoptError:
    print('Error: tsp.py -i <inputfile>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('Help: tsp.py -i <inputfile>')
        sys.exit(2)
    elif opt in ("-i", "--ifile"):
        current_mode = Mode.Test
        path = arg
    elif opt in ("-c", "--ifile"):
        current_mode = Mode.Create
        try:
            size = int(arg)
        except:
            print('tsp.py -c <integer>')
            sys.exit(2)
    else:
        current_mode = Mode.Unknown
        print('Unknown error.')
        sys.exit(2)


# if path == "":
#     print('Missing parameters.')
#     print('tsp.py -i <inputfile>')
#     sys.exit(2)


def parsefile(filepath):
    try:
        mtx = np.loadtxt(filepath, dtype='int')
        print('Input Matrix:\n', mtx)
        return mtx
    except IOError:
        print("Error: file could not be opened")
        sys.exit(2)

def test_matrix():
    matrix = parsefile(path)
    matrix_size = len(matrix)
    bad_matrix = False
    if len(matrix) != len(matrix[0]):
        print('Матрица не квадратная')
        bad_matrix = True

    for i in range(matrix_size):
        if matrix[i][i] != 0:
            print('Даигональ матрицы не 0 в точке ', '[', i, ']', '[', i, ']')
            bad_matrix = True

    for i in range(matrix_size):
        for j in range(matrix_size):
            if matrix[i][j] != matrix[j][i]:
                print('Матрица не зеркальна:')
                print('[', i, ']', '[', j, '] ,', matrix[i][j], '!= ', matrix[j][i], '[', j, ']', '[', i, ']')
                bad_matrix = True
    if bad_matrix is False:
        print('Ошибок в строении матрицы не обнаружено.')

def create_matrix():
    if size <= 0:
        print("Размер матрицы должен быть >0.")
        sys.exit(2)
    matrix = []
    for i in range(size):
        a = []
        for j in range(size):
            if j < i:
                a.append(matrix[j][i])
            elif j == i:
                a.append(0)
            else:
                a.append(random.randint(2,9))
        matrix.append(a)

    filename = 'm' + str(size) + '.txt'
    file = open(filename, 'w')
    for i in range(size):
        for j in range(size):
            file.write(str(matrix[i][j]) + ' ')
        file.write('\n')

if current_mode == Mode.Test:
    test_matrix()
elif current_mode == Mode.Create:
    create_matrix()
