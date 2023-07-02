# Video Scene Extraction

This repository contains scripts for extracting scenes from a video based on different methods. The goal is to identify scene changes and split the video into separate segments representing each scene.

## Methods

1. **Threshold-based scene extraction**: This method compares consecutive frames using the `absdiff` function from the OpenCV library. A threshold is set to determine when a scene change occurs. However, this method may not be very effective in all cases and might not provide accurate scene detection.

2. **Histogram difference-based scene extraction**: This method calculates the histogram difference between consecutive frames using the OpenCV `calcHist` function. By comparing the histogram differences, scene changes can be detected. This method shows better results compared to the first approach, but it still may not be perfect in all scenarios.

3. **Average hash-based scene extraction**: This method utilizes the average hash algorithm to calculate the perceptual hash of each frame. The Hamming distance between consecutive frame hashes is computed to identify scene changes. This approach has proven to be the most effective and reliable in our experiments, providing accurate scene detection.

## Usage

To extract scenes from a video using the preferred method, follow these steps:

1. Clone the repository:
   git clone https://github.com/EBBozkurt/extract_scene.git

2. Install the necessary dependencies:
   pip install -r requirements.txt

3. Replace <video_path> with the path to your video file, and <threshold_value> with the desired threshold value for scene change detection.

4. The extracted scenes will be saved as individual video files in the same directory as the input video.


## Conclusion
Based on our experiments, the average hash-based scene extraction method has shown the most accurate and reliable results. It takes advantage of perceptual hashing to identify scene changes effectively. However, it is important to note that scene extraction can still be a challenging task, and the choice of method may vary depending on the characteristics of the video.

If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.