import os
from .extract_scene import extract_scenes2,get_video_scenes
from .export_to_excel import ExportToExcel

# Main extract scenes from multiple videos class 
class ExtractScenesFMV:
    def __init__(self,path,thresold):

        self.path = path # Arg: mp4 files folder path 
        self.threshold = thresold # Arg: threshold value
        self.directory = os.listdir(path) # All files in the path provided
        self.export = ExportToExcel() # Creating main export to excel object 
        self.videos = [] # Temporary list to store video names for the excel


  
    def extract_scenes_fmv(self): # Extract scene from multiple videos in the provided dir.
        
        # Loop continues for every file in the directory provided
        for file in self.directory:

            extract_scenes2(os.path.join(self.path,file),self.threshold) # Cal extarct_scene2 function
            self.add_to_excel() # Call add excel function after the main extract function


        self.export.close_excel() # Close excel file after the process


    def add_to_excel(self):
        for video in get_video_scenes():
            self.export.add_data_to_table(video) # Add every video name in the list to the excel table

        print(f"{len(get_video_scenes())} row added to excel.") # Inform the user

        get_video_scenes().clear() # Clear the list for every video for the memory efficiency


    

        




