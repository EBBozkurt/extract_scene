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


def add_to_txt(filename: str, values: list):
    """ It can be used for adding arguements to the text file provided
        Args: filename-> name of the file or full path of the file desired
        values -> List of values that will be added to the text file
    """

    # Opens file as write mode
    with open(filename, "w", encoding='utf-8') as file:
        for value in values:  # Loop iterates for every value in the "values" list
            file.write(value+'\n')  # Writes value and goes to the new line


def create_extracted_scenes_files():
    """Create Text File to store all scene files paths"""
    with open("scene_files.txt", "w", encoding="utf-8") as file:  # Open file as write mode
        # Insert 2 empty line. Because the control value start to tag process
        # from 2. This file needs to be sync with the control value.
        file.write(""+"\n"+""+"\n")


def write_extracted_scenes_to_txt(dir: str, subdir: str):
    """
    Write all of the scenes to the txt file
    Args: 
        dir -> Directory name
        subdir -> Sub Directory name
    """
    with open("scene_files.txt", "a", encoding="utf-8") as file:  # Open file as append mode

        # Insert the path with format of 'dir/subdir'
        file.write(os.path.join(dir, subdir)+"\n")


def read_extracted_scenes_files(pos: int):
    """
    Read the scene file path info with the position provided
    Args: pos -> Position(number of line) of the scene to read on the file
    """
    with open("scene_files.txt", "r", encoding="utf-8") as file:  # Open file as read mode
        return file.readlines()[pos][:-1]  # Read except last empty char


def delete_from_extracted_scenes_files(scene_path: str):
    """
    Delete scene path provided from the text file
    Args: scene_path -> Scene file path to delete

    """
    with open("scene_files.txt", "r") as file:  # Open file as read mode
        lines = file.readlines()  # Read all of the lines
    with open("scene_files.txt", "w") as file:  # Open file as write mode
        for line in lines:
            if line.strip("\n") != scene_path:
                # Overwrite all of the scenes except the scene that we want to delete
                file.write(line)


def read_classes_from_txt(path: str):
    """ Read class number and class names from the text file provided\n
        Args: path-> file location of the txt file
        Text file format must be like:
            line 1 nc:3
            line 2 [c1,c2,c3]
    """
    with open(path, "r", encoding="utf-8") as file:  # Open text file with the path provided
        lines = file.readlines()  # Read all of the lines
        # Get first line and get from 3.char to the end of the line
        nc = int(lines[0][3:])
        names_line = lines[1]  # Get second line
        # Get from 7.char to last occurence of ']'. Remove spaces and " ' " characters.
        # Finally, split the result through comma
        names = names_line[7:names_line.rfind("]")].replace(
            " ", "").replace("'", "").split(",")
        return (nc, names)  # Return number of classes and names as tuple


def check_if_all_folder(path: str):
    for i in os.listdir(path):
        if not i.startswith(".") and i != "labels.txt":
            if not os.path.isdir(os.path.join(path, i)):
                return False
    return True
