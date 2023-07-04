import xlsxwriter # Module  for the excel operations

class ExportToExcel:
    def __init__(self):

        # Workbook() takes one, non-optional, argument
        # which is the filename that we want to create.
        self.workbook = xlsxwriter.Workbook('scenes.xlsx')
        self.scene_row = 2

        # The workbook object is then used to add new
        # worksheet via the add_worksheet() method.
        self.worksheet = self.workbook.add_worksheet()

        # It creates Scene Table with Scene Name and Tag Columns
        self.create_scene_table()

    
    def create_scene_table(self):
        
        # Use the worksheet object to write
        # data via the write() method.
        self.worksheet.write('A1', 'Scene Name')
        self.worksheet.write('D1', 'Tag')
        
    
    def add_data_to_table(self,filename):
        # Args: filename-> Filename to add excel table
        self.worksheet.write(f'A{str(self.scene_row)}',filename)
        self.scene_row +=1
    
    def close_excel(self):
        self.workbook.close() # Close the work book for the memory efficiency 



        


    