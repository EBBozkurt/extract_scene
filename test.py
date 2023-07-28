import cv2

from services.file_services import read_extracted_scenes_files

print(read_extracted_scenes_files(2)[:-1][-1])