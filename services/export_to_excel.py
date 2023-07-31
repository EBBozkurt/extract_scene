import os
import openpyxl # Module  for the excel operations

class ExportToExcel:
    """
    This class is used for the export to excel process.
    It exports the scene names to the excel file

    """
    
    def __init__(self):

        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        self.workbook = openpyxl.Workbook()
        self.path = "exported_scenes.xlsx"
        self.scene_row = 2

        if os.path.exists("exported_scenes.xlsx"): # Check the excel file if exists
            os.remove("exported_scenes.xlsx")# It deletes the file

        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        self.worksheet = self.workbook.active # Select worksheet as default
        self.worksheet.title = "Extracted Scenes" # Set worksheet title

        # It creates Scene Table with Scene Name and Tag Columns
        self.create_scene_table()

    
    def create_scene_table(self):
        
        # Use the worksheet object to set values
        self.worksheet["A1"].value = 'Scene Name'
        self.worksheet["B1"].value = '#Frames'
        self.worksheet["C1"].value = 'Tags'
        self.workbook.save(self.path) # Finally, save the excel file

    
    def add_scene_info_to_table(self,filename):
        # Args: filename-> Filename to add excel table
        self.worksheet[f"A{self.scene_row}"].value = filename # Set cell value
        self.workbook.save(self.path) # Finally, save the excel file
        self.scene_row +=1 # Increase row count for every add process
    
        



        


    