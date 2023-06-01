import os
import json
import shutil
from subprocess import PIPE, run
import sys

print("Running")

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE= ["go", "build"]

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
        
def copy_directory_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)
    
def make_json_file(path, game_dir):
    data = {
        "gameNames": game_dir,
        "numberOfGames": len(game_dir)
    }
    with open(path, "w") as f:
        json.dump(data, f)
    

def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break   
    
    if code_file_name is None:
        return
    
    command = GAME_COMPILE + [code_file_name] 
    run_command(command,path)
    
def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)
    
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)    
    print("compile result", result)
    
    os.chdir(cwd)
    
    
    
    
#main ----------------------------------------------------------------                           

def main(source, target):
    cwd = os.getcwd() #gets current working directory
    source_path = os.path.join(cwd, source) # joins source and working directory
    target_path = os.path.join(cwd, target) # joins target and working directory
    
    game_paths = find_all_game_path(source_path)
    new_game_dirs = get_name_of_path(game_paths, "_game")
    print(new_game_dirs)
    

    create_directory(target_path)
    
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_directory_overwrite(src,dest_path)
        compile_game_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")    
    make_json_file(json_path, new_game_dirs,)
    
    #create_directory(target)

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        raise Exception("Must pass a source and target directory - only")
    
    source, target = sys.argv[1:]
    main(source, target)
    
    