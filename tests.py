import os
import sys
import subprocess

path = 'tests/input/'
result_path = 'tests/tests.txt'

print(os.getcwd() + '/' + path)

if os.path.exists(result_path):
    print('File tests.txt already exists, rewrite? (y or n)')
    input_string = input()
    answer = ''
    try:
        answer = str(input_string)
    except:
        print('Wrong input')
        sys.exit(2)
    if answer == 'y':
        file = open(result_path, 'w')
        file.close()


for filename in os.listdir(os.getcwd() + '/' + path):
    if filename.endswith(".txt"):
        call = "python3.9 tsp.py -i " + path + filename + " -t"
        print(call)
        subprocess.call(call, shell=True)

file = open(result_path, 'r')
print("\nResults:")
for line in file:
    print(line.strip())