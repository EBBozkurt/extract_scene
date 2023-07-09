import json

# Important reminder!! Do not make any change on the 'control.json' file by hand.


# Class for the control.json file operations.
# Purpose of the control.json : This json file stores just one value called 'control'
# This control value indicates the status of the program.
# 0 means the program did not take any input from user
# 1 means the program has taken before extraction inputs
# control > 1 indicates number of scenes completed.
# For example: The user typed all of the inputs and checked 12 scene and terminated the program.
# In this situation, the control value would be 12. If the user start the program again the program will
# be continued from scene 12. 
class JsonControl:

    def __init__(self):

        # Opens json file and stores as dictionary in the 'data' variable
        with open('control.json','r') as jfile:
            self.data = json.load(jfile)             
        

    def check_control(self):
        """Returns control value as integer"""
        return self.data["control"]
    
    def increase_control(self):
        """Increases control value"""
        self.data["control"] += 1

        """Finally, overwrites the control value to control.json file"""
        with open('control.json','w') as jfile:
            json.dump(self.data,jfile)
    
    def reset_control(self):
        """
            Sets 0 to control value. Be careful to use this function!!\n
            You may lose your progress
        """
        self.data["control"] = 0

        #Finally, overwrites the control value to control.json file
        with open('control.json','w') as jfile:
            json.dump(self.data,jfile)
    