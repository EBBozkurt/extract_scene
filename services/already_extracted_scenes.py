import os
from services.file_services import check_if_all_folder
from services.export_to_excel import ExportToExcel

class AlreadyExtractedScenes:
    def __init__(self,master_path):
        self.master_path = master_path
        self.excel_control = ExportToExcel()
        self.excel_control.create_scene_table()


    def add_to_excel(self):
        for directory in os.listdir(self.master_path):
            if not directory.startswith(".") and directory != "labels.txt":
                for subDir in os.listdir(os.path.join(self.master_path,directory)):
                    if not subDir.startswith(".") :
                        self.excel_control.add_scene_info_to_table(subDir[:subDir.rfind(".")])
            if not directory.startswith(".") and directory != "labels.txt":
                print(f"Scenes for {directory} added to excel")


