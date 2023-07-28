import os
from services.file_services import check_if_all_folder, create_extracted_scenes_files, write_extracted_scenes_to_txt
from services.export_to_excel import ExportToExcel

# This class will be used if the user choose to skip extract scene process
class AlreadyExtractedScenes:
    def __init__(self,master_path):
        self.master_path = master_path # Name of the master folder contains extracted scenes

        self.excel_control = ExportToExcel() # It calls ExportToExcel class
        self.excel_control.create_scene_table()
        create_extracted_scenes_files()


    def add_to_excel(self):
        for directory in os.listdir(self.master_path):
            if not directory.startswith(".") and directory != "labels.txt":
                for subDir in os.listdir(os.path.join(self.master_path,directory)):
                    if not subDir.startswith(".") :
                        self.excel_control.add_scene_info_to_table(subDir[:subDir.rfind(".")])
                        write_extracted_scenes_to_txt(directory,subDir)

            if not directory.startswith(".") and directory != "labels.txt":
                print(f"Scenes for {directory} added to excel")


