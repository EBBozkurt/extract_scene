import json
from services.extract_scene_from_multiple_videos import ExtractScenesFMV
from services.file_services import check_directory,JsonControl,add_to_txt

# Main program process class. All of the processes will be executed through this class
class StartProcess:
    def __init__(self):
        self.start_main_program()

        
    def start_main_program(self):
        self.control = JsonControl() # Call json object from file_services
    
        while True:
            if self.control.check_control() == -1: # Check control value and execute accordingly
                self.input_before_extract() # Execute first input process
                extract = ExtractScenesFMV(self.video_path,self.threshold) # Call ExtractScenesFMV object with the corresponding args
                extract.extract_scenes_fmv() # Execute extract process which is using the extract_scene_2 function

            elif self.control.check_control() == 0:
                self.input_after_extract() # Execute after extract process
            else:
                break # It will be implemented later

    def input_before_extract(self):
        while True:

            # Take path input from the user 
            self.video_path = input("Enter the path of the directory containing the mp4s:")

            # Try to call the function. If there is a error, inform the user.
            try:
                if not check_directory(self.video_path):
                    print("All of the files in the directory provided must be mp4!")
                    continue
            except:
                print("Folder not found!")
                continue

            self.threshold = int(input("Enter the thresold: ") or 20)
            break   

        self.control.increase_control() # The first input process has been ended. Increase the control value.


    def input_after_extract(self):

        while True: # Main input process loop
            number_of_class = input("Enter number of class:") 
            try: 
                number_of_class = int(number_of_class) # Try to convert the input value to the int value
                break # If there is no error, break the loop
            except:
                print("Error! Please type integer value.")
                continue # If there is a error, inform the user and start the loop again
    
        class_names = [] # List variable  that stores name of classes will be provided

        for i in range(1,number_of_class+1): # Execute exactly number of classes provided and start from 1
            class_name = input(f"Enter class name {i}:") 
            class_names.append(class_name) # Add class name input provided from the user to the list

        # Execute add_to_txt function from file_services with the corresponding args 
        add_to_txt(
            "extracted_scenes/labels.txt",
            [
                f"nc:{number_of_class}",
                f"names:{class_names}",
            ]
        )
        self.control.increase_control() # The second input process has been ended. Increase the control value. 

        
        
            
            


    