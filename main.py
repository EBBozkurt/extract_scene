from services.extract_scene_from_multiple_videos import ExtractScenesFMV
from services.file_services import check_directory
import os
from services.json_control import JsonControl

from services.start_process import StartProcess




# Threshold-based scene extraction
# threshold = 9800000
# extract_scenes(video_path, threshold)

# Histogram difference-based scene extraction
# threshold = 0.55
# extract_scenes1(video_path, threshold)

# Starts main program process
# It uses average hash-based scene extraction
process = StartProcess()
