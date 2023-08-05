import os
from services.export_to_excel import ExportToExcel
from services.file_services import create_extracted_scenes_files, write_extracted_scenes_to_txt

# This class will be used if the user choose to skip extract scene process


class AlreadyExtractedScenes:
    def __init__(self, master_path):
        # Name of the master folder contains extracted scenes
        self.master_path = master_path
        self.excel_control = ExportToExcel()  # It calls ExportToExcel class
        self.excel_control.create_scene_table()  # Create scene tables to excel
        create_extracted_scenes_files()  # Create a txt file stores path of the scenes

    def add_to_excel(self):
        """Adds all of the scenes of each videos to the excel file"""

        # List of video directories
        video_directory_list = os.listdir(self.master_path)

        for directory in video_directory_list:  # Traverse for every video

            # Ignore any hidden file like .DS_STORE and labels.txt file
            if not directory.startswith(".") and directory != "labels.txt":

                # Path of directory
                directory_path = os.path.join(self.master_path, directory)

                if os.path.isdir(directory_path):
                    # Traverse for every scenes

                    # List of extracted scenes
                    scene_list = os.listdir(directory_path)

                    for subDir in scene_list:

                        # Ignore any hidden file like .DS_STORE
                        if not subDir.startswith("."):
                            # Add to excel except last char which is empty char
                            self.excel_control.add_scene_info_to_table(
                                subDir[:subDir.rfind(".")])

                            # Add full path to txt file
                            write_extracted_scenes_to_txt(directory, subDir)

            # Ignore any hidden file like .DS_STORE and labels.txt file
            if not directory.startswith(".") and directory != "labels.txt":
                # Inform the user
                print(f"Scenes for {directory} added to excel")
