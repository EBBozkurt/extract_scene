import os
import cv2
from services.extract_scene_from_multiple_videos import ExtractScenesFMV
from services.file_services import check_directory, add_to_txt, read_classes_from_txt
from services.json_control import JsonControl
from services.excel_control import ExcelControl

# Main program process class. All of the processes will be executed through this class
class StartProcess:
    def __init__(self):
        self.current_dir = os.getcwd() # Get current dir

        self.control = JsonControl() # Call json object from JsonControl
        self.start_main_program()

        
    def start_main_program(self):
        """
        Start main program process.\n
        This function checks control value from json and calls corresponding function
        """
    
        while True:
            match self.control.check_control():
                case  0: # Check control value and execute accordingly
                    self.input_before_extract() # Execute first input process
                    extract = ExtractScenesFMV(self.video_path,self.threshold) # Call ExtractScenesFMV object with the corresponding args
                    extract.extract_scenes_fmv() # Execute extract process which is using the extract_scene_2 function
                    
                    # Call excel object from ExcelControl with the corresponding args
                    self.excel = ExcelControl(
                        os.path.join(self.current_dir,"exported_scenes.xlsx"),
                        "Sheet1"
                    )


                case 1:
                    self.input_after_extract() # Execute after extract process
                
                case _: # Execute this case if none of the case above execute
                    
                    # Call excel object from ExcelControl with the corresponding args
                    self.excel = ExcelControl(
                        os.path.join(self.current_dir,"exported_scenes.xlsx"),
                        "Sheet1"
                    )

                    # Inform the user if control value reach to the row_count +1 
                    # (+1 comes from input process. +1 added to the control value when input_after_extract executed)
                    if self.control.check_control() == self.excel.get_row_count_from_excel() + 1:
                        print("All scenes classified")
                        break # Program termination point

                    self.show_video_process() # Execute video process after input processes
                    break # Program termination point

 


    def input_before_extract(self):
        """
        This function takes first input values from the user.
        If this function is executed, the value of control = 0

        """
        
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
        """
        This function takes second input values from the user.
        If this function is executed, the value of control = 1

        """
        while True: # Main input process loop
            number_of_class = input("Enter number of class(between 1-10):")
  
            try: 
                number_of_class = int(number_of_class) # Try to convert the input value to the int value
                if number_of_class <= 0 or number_of_class > 10: # Check if the entered value is within the range
                    print("Please type number of class between 1 and 10")
                    continue

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
            os.path.join(self.current_dir,"extracted_scenes","labels.txt"),
            [
                f"nc:{number_of_class}",
                f"names:{class_names}",
            ]
        )
        self.control.increase_control() # The second input process has been ended. Increase the control value. 

    def show_video_process(self):
        """
        This function shows extracted scenes to the user.\n
        And takes scene class inputs from the user. \n
        Finally, writes these inputs to the excel simultaneously.\n
        If the user terminates the program at some point,\n
        the program will continue from that point.
        If this function is executed, the value of 2 <= control <= row_count_from_excel

        """

        # Read class names and number of classes from the txt file provided
        classes =read_classes_from_txt(os.path.join(self.current_dir,"extracted_scenes","labels.txt"))
 
        # Get row count from the excel file provided
        row_count = self.excel.get_row_count_from_excel()

        # Repeat the process exactly the row_count
        for i in range(self.control.check_control(),row_count+1):

            
            # Read scene file name from the cell provided
            scene_file_name = self.excel.read_from_excel(f"A{i}")

            # Create same scene folder name with the corresponding scene to find exact location of it
            scene_file_dir = f"{scene_file_name[:scene_file_name.index('_scene')]}_scenes"

            # Add .mp4 to the end to find location properly
            scene_file = scene_file_name + ".mp4"

            # Specify the target width and height for resizing
            target_width = 500
            target_height = 500

            # Get scene video from the path provided
            cap = cv2.VideoCapture(os.path.join(self.current_dir,"extracted_scenes",scene_file_dir,scene_file))
            # Get the original video's width and height
            original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Check if the original dimensions are non-zero
            if original_width > 0 and original_height > 0:
                # Calculate the aspect ratio of the original video
                aspect_ratio = original_width / original_height

            # Calculate the resized width and height while maintaining the aspect ratio
            if aspect_ratio > 1:
                resized_width = target_width
                resized_height = int(target_width / aspect_ratio)
            else:
                resized_height = target_height
                resized_width = int(target_height * aspect_ratio)

            # Check if video opened successfully
            if (cap.isOpened()== False): 
                print("Error opening video stream or file")

            # Create numbers list to combine with the class names
            numbers = [ "0" if i==10 else str(i)  for i in range(1,classes[0]+1)]
           
            # Create number_ords list containing ord values of the numbers
            # It will be used for the pressed key constraints
            numbers_ords = list(map(ord,numbers))

            # Add 113 which means ord value of the 'q'. Because 'q' value will be allowed always
            numbers_ords.append(113)

            # Combine class names with the numbers
            classes_with_numbers = list(zip(numbers,classes[1]))

            #Inform the user with the number of classes 
            print(f"You have {classes[0]} options. Press one of them. Press 'q' to quit")

            # Print class names with the numbers line-by-line to inform the user
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
                # Resize the frame to the target width and height while maintaining the aspect ratio
                resized_frame = cv2.resize(frame, (resized_width, resized_height))
                # Display the frame
                cv2.imshow(scene_file_name, resized_frame)

                # Wait for a key press (waitKey returns the pressed key)
                key = cv2.waitKey(25)  # 25 millisecond delay

                # Check if any key was pressed (key value is not -1)
                if key != -1:
                    if key not in numbers_ords : # Check key if in the allowed keys or not
                            print("Your input is invalid. Check out the number values from the console.")
                            continue # Restart the while loop
                    match key: # Check all possibility of the pressed key. Case values are ord values of the keys 
                        case 49: # If pressed 1

                            # Add class number to the "tags" column of the scene through add_to_excel func.
                            self.excel.add_to_excel(f"D{i}","0")
                            print("Class number 0 added to excel")
             
                        case 50: # If pressed 2
                            self.excel.add_to_excel(f"D{i}","1")
                            print("Class number 1 added to excel")
    
                        case 51: # If pressed 3
                            self.excel.add_to_excel(f"D{i}","2")
                            print("Class number 2 added to excel")
                  
                        case 52: # If pressed 4
                            self.excel.add_to_excel(f"D{i}","3")
                            print("Class number 3 added to excel")
                 
                        case 53: # If pressed 5
                            self.excel.add_to_excel(f"D{i}","4")
                            print("Class number 4 added to excel")
            
                        case 54: # If pressed 6
                            self.excel.add_to_excel(f"D{i}","5")
                            print("Class number 5 added to excel")
        
                        case 55: # If pressed 7
                            self.excel.add_to_excel(f"D{i}","6")
                            print("Class number 6 added to excel")
                   
                        case 56: # If pressed 8
                            self.excel.add_to_excel(f"D{i}","7")
                            print("Class number 7 added to excel")
         
                        case 57: # If pressed 9
                            self.excel.add_to_excel(f"D{i}","8")
                            print("Class number 8 added to excel")
  
                        case 48: # If pressed 0
                            self.excel.add_to_excel(f"D{i}","9")
                            print("Class number 9 added to excel")
            
                        case 113: # If pressed q, return 0 (terminate the function)
                            print("Exited. Your progress has been saved")
                            return 0
                
                    cv2.destroyAllWindows() # Closes all the frames
                    break

            #  The classification process for this scene has been ended. Increase the control value. 
            self.control.increase_control()
  
        # When everything done, release the video capture object
        cap.release()
        print("Classification is done!")
        
                
        
            
            


    