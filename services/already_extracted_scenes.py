import os
from services.export_to_excel import ExportToExcel
from services.file_services import create_extracted_scenes_files, write_extracted_scenes_to_txt

# This class will be used if the user choose to skip extract scene process
class AlreadyExtractedScenes:
    def __init__(self,master_path):
        self.master_path = master_path # Name of the master folder contains extracted scenes
        self.excel_control = ExportToExcel() # It calls ExportToExcel class
        self.excel_control.create_scene_table() # Create scene tables to excel
        create_extracted_scenes_files() # Create a txt file stores path of the scenes


    def add_to_excel(self):
        """Adds all of the scenes of each videos to the excel file"""
        for directory in os.listdir(self.master_path): # Traverse for every video
            # Ignore any hidden file like .DS_STORE and labels.txt file 
            if not directory.startswith(".") and directory != "labels.txt":
                for subDir in os.listdir(os.path.join(self.master_path,directory)): # Traverse for every scenes
                    if not subDir.startswith(".") : # Ignore any hidden file like .DS_STORE
                        self.excel_control.add_scene_info_to_table(subDir[:subDir.rfind(".")]) # Add to excel except last char which is empty char
                        write_extracted_scenes_to_txt(directory,subDir) # Add full path to txt file

            if not directory.startswith(".") and directory != "labels.txt": # Ignore any hidden file like .DS_STORE and labels.txt file
                print(f"Scenes for {directory} added to excel") # Inform the user

            



