import os

def print_tree(start_path, depth=2, indent=''):
    if depth < 0:
        return
    for item in os.listdir(start_path):
        path = os.path.join(start_path, item)
        print(indent + '├── ' + item)
        if os.path.isdir(path):
            print_tree(path, depth-1, indent + '│   ')

print_tree('.', depth=2)