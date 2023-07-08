import cv2
from services.extract_scene_from_multiple_videos import ExtractScenesFMV
from services.file_services import (add_to_excel, check_directory,JsonControl,
                                    add_to_txt, get_row_count_from_excel, read_classes_from_txt, 
                                    read_from_excel)

# Main program process class. All of the processes will be executed through this class
class StartProcess:
    def __init__(self):
        self.excel_path = "/Users/yusufs/Desktop/extract_scene/exported_scenes.xlsx"
        self.start_main_program()

        
    def start_main_program(self):
        self.control = JsonControl() # Call json object from file_services
    
        while True:
                match self.control.check_control():
                    case  0: # Check control value and execute accordingly
                        self.input_before_extract() # Execute first input process
                        extract = ExtractScenesFMV(self.video_path,self.threshold) # Call ExtractScenesFMV object with the corresponding args
                        extract.extract_scenes_fmv() # Execute extract process which is using the extract_scene_2 function

                    case 1:
                        self.input_after_extract() # Execute after extract process
                    
                    case _:
                        if self.control.check_control() <= get_row_count_from_excel(self.excel_path,"Sheet1"):
                            self.show_video_process()
                        else:
                            print("All scenes classified!")
                            break
            


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

    def show_video_process(self):

        classes =read_classes_from_txt("/Users/yusufs/Desktop/extract_scene/extracted_scenes/labels.txt")
        excel_path = "/Users/yusufs/Desktop/extract_scene/exported_scenes.xlsx"
        row_count = get_row_count_from_excel(excel_path,"Sheet1")
        for i in range(self.control.check_control(),row_count+1):
            scene_file_name = read_from_excel(
                excel_path,
                "Sheet1",
                f"A{i}"
            )
            scene_file_dir = f"{scene_file_name[:scene_file_name.index('_scene')]}_scenes"
            scene_file = scene_file_name + ".mp4"


            cap = cv2.VideoCapture(f"/Users/yusufs/Desktop/extract_scene/extracted_scenes/{scene_file_dir}/{scene_file}")

            # Check if video opened successfully
            if (cap.isOpened()== False): 
                print("Error opening video stream or file")

            numbers = [i for i in range(1,classes[0])]
            classes_with_numbers = list(zip(numbers,classes[1]))
            print(f"You have {classes[0]} options. Press one of them.")
            [print(c) for c in classes_with_numbers]

            # Read until video is completed
            while True:
                # Read the next frame from the video
                ret, frame = cap.read()

                # Check if the frame was successfully read
                if not ret:
                    # Restart the video from the beginning
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue

                # Display the frame
                cv2.imshow(scene_file_name, frame)

                # Wait for a key press (waitKey returns the pressed key)
                key = cv2.waitKey(25)  # 1 millisecond delay
                # Check if any key was pressed (key value is not -1)
                if key != -1:
                    if key != 113:
                        if key > ord(f"{classes[0]}") or key< ord("1"):
                            print("Your input is out of range. Check out the number values from the console.")
                            continue
                    match key:
                        case 49:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","0")
             
                        case 50:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","1")
    
                        case 51:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","2")
                  
                        case 52:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","3")
                 
                        case 53:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","4")
            
                        case 54:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","5")
        
                        case 55:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","6")
                   
                        case 56:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","7")
         
                        case 57:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","8")
  
                        case 48:
                            add_to_excel(excel_path,"Sheet1",f"D{i}","9")

                        case 113:
                            return 0
                

                    cv2.destroyAllWindows()
                    break
            self.control.increase_control()

                     
                    
                
        # When everything done, release the video capture object
        cap.release()
            
        # Closes all the frames
        
        self.control.increase_control()
                
        
            
            


    