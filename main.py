from services.extract_scene_from_multiple_videos import ExtractScenesFMV
from services.file_services import check_directory
import os



while True:

    # Take path input from the user 
    video_path = input("Enter the path of the directory containing the mp4s:")

    # Try to call the function. If there is a error, inform the user.
    try:
        if not check_directory(video_path):
            print("All of the files in the directory provided must be mp4!")
            continue
    except:
        print("Folder not found!")
        continue

    threshold = int(input("Enter the thresold: ") or 20)
    break


# Threshold-based scene extraction
# threshold = 9800000
# extract_scenes(video_path, threshold)

# Histogram difference-based scene extraction
# threshold = 0.55
# extract_scenes1(video_path, threshold)


# Average hash-based scene extraction
extract = ExtractScenesFMV(video_path,20)
extract.extract_scenes_fmv()
