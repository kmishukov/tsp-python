import os
import subprocess

path = 'tests/input/'

print(os.getcwd()+ path)

for filename in os.listdir(os.getcwd() + '/' + path):
    if filename.endswith(".txt"):
        print(path + filename)
        call = "python3.9 tsp.py -i " + path + filename + " -t"
        print(call)
        subprocess.call(call, shell=True)