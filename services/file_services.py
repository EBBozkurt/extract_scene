import os
import shutil


def check_directory(path):

    # Args: path -> path from the user input
    # Check directory if exists or not. And also check all of the files are mp4.
    # It returns True if available for the extract_scene process.
    # Otherwise it returns False or FileNotFoundError if the folder provided not exists
    # Also delete the "extracted_scenes" folder if exists.
    # Because, the name of the folder which contains extracted scenes will be "extracted_scenes"

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

    # Extracts the file name from the path
    video_name = os.path.basename(video_path)

    video_name_without_extension = os.path.splitext(
        video_name)[0]  # Removes the file extension

    return video_name_without_extension
