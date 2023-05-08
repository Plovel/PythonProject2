import os
import shutil

PROJECT_NAME = "game.py"
PATH_FOR_OUTPUT = "build/"
PATH_TO_SRC = "src/"
FILES_SEQUENCE = ["constants",
                  "pygame_init",
                  "global_zone",
                  "draw", "game_core",
                  "sessions",
                  "gamemodes",
                  "menu",
                  "handlers",
                  "main"]

if os.path.isdir(PATH_FOR_OUTPUT):
    if os.path.isfile(PATH_FOR_OUTPUT + PROJECT_NAME):
        os.remove(PATH_FOR_OUTPUT + PROJECT_NAME)
    if os.path.isdir(PATH_FOR_OUTPUT + "media"):
        shutil.rmtree(PATH_FOR_OUTPUT + "media")
else:
    os.mkdir(PATH_FOR_OUTPUT)

IMPORT_MESSAGE_LEN = 70
def ToPrint(message):
    left = (IMPORT_MESSAGE_LEN - 1 - len(message)) // 2
    right = IMPORT_MESSAGE_LEN - 1 - len(message) - left
    return ('#' + '-' * left + message + '-' * right)

with open(PATH_FOR_OUTPUT + PROJECT_NAME, 'w') as project:
    def AddFile(filename):
        first_message = filename + " BEGIN"
        second_message = filename + " END"
        with open(filename, 'r') as file:
            print(ToPrint(first_message), file=project)
            print(file.read(), file=project)
            print(ToPrint(second_message), file=project)

    for filename in FILES_SEQUENCE:
        AddFile(PATH_TO_SRC + filename + ".py")

shutil.copytree(PATH_TO_SRC + "media", PATH_FOR_OUTPUT + "media/")
