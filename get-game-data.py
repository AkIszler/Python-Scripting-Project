import os
import json
import shutil
from subprocess import PIPE, run
import sys

print("Running")

GAME_DIR_PATTERN = "game"

def find_all_game_path(source):
    game_path = []
    
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_path.append(path)
                
        break
    
    return game_path

def get_name_of_path(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
        
    return new_names

def create_directory(path):
    if not os.path.exists(path):
        os.mkdir(path)

def main(source, target):
    cwd = os.getcwd() #gets current working directory
    source_path = os.path.join(cwd, source) # joins source and working directory
    target_path = os.path.join(cwd, target) # joins target and working directory
    
    game_paths = find_all_game_path(source_path)
    new_game_dirs = get_name_of_path(game_paths, "game")
    print(new_game_dirs)
    create_directory(target)

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        raise Exception("Must pass a source and target directory - only")
    
    source, target = sys.argv[1:]
    main(source, target)
    
    