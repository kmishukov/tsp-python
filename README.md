# TSP-Python

## This program is used to solve symmetric Traveling Salesman Problem using branch and bound technique. Traveling sales problem is a task to find shortest route to visit all points without using same road more than once and return to origin.

### Install requirements:

``pip install -r requirements.txt``

### Matrix prerequesites: 

- Matrix must be symmetric and in a .txt file.
### 10x10 matrix example:
``0 3 5 7 6 5 9 8 8 9``\
``3 0 8 6 7 8 7 4 7 9``\
``5 8 0 2 7 4 6 9 7 2``\
``7 6 2 0 5 8 7 4 2 5``\
``6 7 7 5 0 8 9 2 6 5``\
``5 8 4 8 8 0 8 6 5 5``\
``9 7 6 7 9 8 0 4 5 7``\
``8 4 9 4 2 6 4 0 4 2``\
``8 7 7 2 6 5 5 4 0 4``\
``9 9 2 5 5 5 7 2 4 0``

### Usage example:

``python3.9.exe tsp.py -i matrix.txt``

### Sample output:

``Best solution: 38.0``  
``Solution path: 0-5-2-9-4-7-6-8-3-1-0``  
``Time elapsed: 3.958 seconds``
