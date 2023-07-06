from services.extract_scene import extract_scenes2

video_path = "SnakeEatingInsect.mp4"


# Threshold-based scene extraction
# threshold = 9800000
# extract_scenes(video_path, threshold)

# Histogram difference-based scene extraction
# threshold = 0.55
# extract_scenes1(video_path, threshold)


# Average hash-based scene extractionn
threshold = 20
extract_scenes2(video_path, threshold)
