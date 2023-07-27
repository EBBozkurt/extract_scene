import os
import shutil

def check_directory(path):
    """
     Args: path -> path from the user input
     Check directory if exists or not. And also check all of the files are mp4.
     It returns True if available for the extract_scene process.
     Otherwise it returns False or FileNotFoundError if the folder provided not exists
     Also delete the "extracted_scenes" folder if exists.
     Because, the name of the folder which contains extracted scenes will be "extracted_scenes"
    """
    if os.path.exists("extracted_scenes"):  # Check the file name if exists
        # It deletes the directory include files within that directory
        shutil.rmtree("extracted_scenes")
    
    if os.path.exists("exported_scenes.xlsx"): # Check the excel file if exists
        # It deletes the file
        os.remove("exported_scenes.xlsx")

    for file in os.listdir(path):
        if not os.path.isdir(path):
            return FileNotFoundError
        if not file.endswith(".mp4"):
            return False
    return True


def get_video_name_from_given_path(video_path) -> str:
    """
    Returns the video name from the full path
    """
    # Extracts the file name from the path
    video_name = os.path.basename(video_path)

    video_name_without_extension = os.path.splitext(
        video_name)[0]  # Removes the file extension

    return video_name_without_extension





def add_to_txt(filename : str, values : list ):
    """ It can be used for adding arguements to the text file provided
        Args: filename-> name of the file or full path of the file desired
        values -> List of values that will be added to the text file
    """

    # Opens file as write mode
    with open(filename,"w",encoding='utf-8') as file:
        for value in values: # Loop iterates for every value in the "values" list
            file.write(value+'\n') # Writes value and goes to the new line



def read_classes_from_txt(path):
    """ Read class number and class names from the text file provided\n
        Args: path-> file location of the txt file
        Text file format must be like:
            line 1 nc:3
            line 2 [c1,c2,c3]
    """
    with open(path,"r",encoding="utf-8") as file: # Open text file with the path provided
        lines = file.readlines() # Read all of the lines
        nc = int(lines[0][3:]) # Get first line and get from 3.char to the end of the line
        names_line = lines[1] # Get second line
        # Get from 7.char to last occurence of ']'. Remove spaces and " ' " characters.
        # Finally, split the result through comma  
        names = names_line[7:names_line.rfind("]")].replace(" ","").replace("'","").split(",")
        return (nc,names) # Return number of classes and names as tuple
    

def check_if_all_folder(path : str):
    for i in os.listdir(path):
        if not i.startswith(".") and i != "labels.txt":
            if not os.path.isdir(os.path.join(path,i)):
                return False
    return True


            