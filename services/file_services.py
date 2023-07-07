import json
import os
import shutil

def check_directory(path):

    # Args: path -> path from the user input
    # Check directory if exists or not. And also check all of the files are mp4.
    # It returns True if available for the extract_scene process.
    # Otherwise it returns False or FileNotFoundError if the folder provided not exists
    # Also delete the "extracted_scenes" folder if exists.
    # Because, the name of the folder which contains extracted scenes will be "extracted_scenes"
    
    
    if os.path.exists("extracted_scenes"): # Check the file name if exists
    # It deletes the directory include files within that directory
        shutil.rmtree("extracted_scenes")

    for file in os.listdir(path):
        if not os.path.isdir(path):
            return FileNotFoundError
        if not file.endswith(".mp4"):
            return False
    return True

# Class for the control.json file operations.
# Purpose of the control.json : This json file stores just one value called 'control'
# This control value indicates the status of the program.
# -1 means the program did not take any input from user
#  0 means the program has taken before extraction inputs
#  control > 0 indicates number of scenes completed.
#  For example: The user typed all of the inputs and checked 12 scene and terminated the program.
#  In this situation, the control value would be 12. If the user start the program again the program will
#  be continued from scene 12. 
class JsonControl:

    def __init__(self):

        # Opens json file and stores as dictionary in the 'data' variable
        with open('control.json','r') as jfile:
            self.data = json.load(jfile)             
        

    def check_control(self):
        # Returns control value as integer
        return self.data["control"]
    
    def increase_control(self):
        # Increases control value
        self.data["control"] += 1

        # Finally, overwrites the control value to control.json file
        with open('control.json','w') as jfile:
            json.dump(self.data,jfile)
        


def add_to_txt(filename : str, values : list ):
    # It can be used for adding arguements to the text file provided
    # Args: filename-> name of the file or full path of the file desired
    #       values -> List of values that will be added to the text file

    # Opens file as write mode
    with open(filename,"w",encoding='utf-8') as file:
        for value in values: # Loop iterates for every value in the "values" list
            file.write(value+'\n') # Writes value and goes to the new line

