import cv2
import imagehash
from PIL import Image
import os
import shutil

video_count = 1 # Global video count variable for the increase_video_count function
video_name = [] # Global video name variable for the get_video_name function

def increase_video_count():
    # It increases global video_count variable
    # This function is used for the multiple video scenes naming
    global video_count
    video_count +=1

def get_video_name():
    # It returns video_name variable. Empty list will be loaded with the current video name
    # This function is used for store the video names temporarily
    return video_name

def extract_scenes(video_path: str, scene_threshold: int):
    """
    Extracts scenes from a video based on a specified threshold.

    Args:
        video_path (str): Path to the video file.
        scene_threshold (int): Threshold for scene change detection.

    Returns:
        None
    """

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, prev_frame = video.read()
    if not ret:
        print("Error reading the video file.")
        return

    # Initialize variables
    scene_count = 0
    frame_count = 0

    # Define the codec for the output video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Initialize video writer for the first scene
    scene_filename = f"scene_0.mp4"
    scene_writer = cv2.VideoWriter(
        scene_filename, fourcc, 30, (prev_frame.shape[1], prev_frame.shape[0]))

    # Write the first frame to the scene video file
    scene_writer.write(prev_frame)

    # Convert the first frame to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        # Read the next frame
        ret, frame = video.read()
        if not ret:
            break

        # Convert frames to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate absolute difference between frames
        frame_diff = cv2.absdiff(prev_gray, gray)
        diff_sum = frame_diff.sum()

        # Check if a scene change has occurred
        if diff_sum > scene_threshold:
            scene_count += 1
            print(f"Scene change detected at frame {frame_count}")

            # Release the previous scene writer
            scene_writer.release()

            # Define the output video file name
            scene_filename = f"scene_{scene_count}.mp4"

            # Initialize the scene writer
            scene_writer = cv2.VideoWriter(
                scene_filename, fourcc, 30, (frame.shape[1], frame.shape[0]))

        # Write the frame to the scene video file
        scene_writer.write(frame)

        # Update the previous frame
        prev_gray = gray.copy()

        # Increment frame count
        frame_count += 1

    # Release the scene writer and video capture objects
    scene_writer.release()
    video.release()


def extract_scenes1(video_path: str, threshold: float):
    """
    Extracts scenes from a video based on histogram difference shot boundary detection.

    Args:
        video_path (str): Path to the video file.
        threshold (float): Threshold for shot boundary detection.

    Returns:
        None
    """

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, prev_frame = video.read()
    if not ret:
        print("Error reading the video file.")
        return

    # Convert the first frame to grayscale
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_hist = cv2.calcHist([prev_gray], [0], None, [256], [0, 256])
    prev_hist = cv2.normalize(prev_hist, prev_hist).flatten()

    # Initialize variables
    scene_count = 0
    frame_count = 0
    scene_writer = None

    # Handle the first scene separately
    scene_count += 1
    print(f"Scene {scene_count} starts at frame {frame_count}")

    # Define the output video file name
    scene_filename = f"scene_{scene_count}.mp4"

    # Initialize the scene writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    scene_writer = cv2.VideoWriter(
        scene_filename, fourcc, 30, (prev_frame.shape[1], prev_frame.shape[0]))
    scene_writer.write(prev_frame)

    while True:
        # Read the next frame
        ret, frame = video.read()
        if not ret:
            break

        # Convert frames to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Calculate histogram of the current frame
        curr_hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        curr_hist = cv2.normalize(curr_hist, curr_hist).flatten()

        # Calculate histogram difference
        hist_diff = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_CORREL)

        # Check if a shot boundary has occurred
        if hist_diff < threshold:
            scene_count += 1
            print(f"Scene {scene_count} starts at frame {frame_count}")

            if scene_writer is not None:
                # Release the previous scene writer
                scene_writer.release()

            # Define the output video file name
            scene_filename = f"scene_{scene_count}.mp4"

            # Initialize the scene writer
            scene_writer = cv2.VideoWriter(
                scene_filename, fourcc, 30, (frame.shape[1], frame.shape[0]))

        # Write the frame to the scene video file
        if scene_writer is not None:
            scene_writer.write(frame)

        # Update the previous histogram
        prev_hist = curr_hist

        # Increment frame count
        frame_count += 1

    # Release the scene writer and video capture objects
    if scene_writer is not None:
        scene_writer.release()

    video.release()

def extract_scenes2(video_path: str, threshold: int):
    """
    Extracts scenes from a video based on average hash algorithm.

    Args:
        video_path (str): Path to the video file.
        threshold (int): Threshold for scene change detection.

    Returns:
        None
    """
    global video_count # For using the global video count
    global video_name # For using the global video name

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Read the first frame
    ret, prev_frame = video.read()
    if not ret:
        print("Error reading the video file.")
        return

    # Compute the average hash of the first frame
    prev_hash = imagehash.average_hash(Image.fromarray(prev_frame))

    # Initialize variables
    scene_count = 1
    frame_count = 0
    scene_writer = None

    # Define the output video file name
    scene_filename = f"video_{video_count}_scene_{scene_count}.mp4"
    video_name.append(scene_filename)

    # Create a directory for the scenes extracted.
    # If there is a folder with that name. Delete it.
    scenes_folder = f"video_{video_count}_scenes"
    if os.path.exists(scenes_folder):
        shutil.rmtree(scenes_folder)
    os.makedirs(scenes_folder)

    # Initialize the scene writer
   
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    scene_writer = cv2.VideoWriter(
        os.path.join(scenes_folder,scene_filename), fourcc, 30, (prev_frame.shape[1], prev_frame.shape[0]))
    
    scene_writer.write(prev_frame)
    print(f"Video {video_count} Scene {scene_count} extracted")
    


    while True:
        # Read the next frame
        ret, frame = video.read()
        if not ret:
            break

        # Compute the average hash of the current frame
        curr_hash = imagehash.average_hash(Image.fromarray(frame))

        # Calculate the Hamming distance between the hashes
        hash_diff = prev_hash - curr_hash

        # Check if a scene change has occurred
        if hash_diff > threshold:
            scene_count += 1
            print(f"Video {video_count} Scene {scene_count} extracted")

            if scene_writer is not None:
                # Release the previous scene writer
                scene_writer.release()

            # Define the output video file name
            scene_filename = f"video_{video_count}_scene_{scene_count}.mp4"
            video_name.append(scene_filename)
            # Initialize the scene writer
            scene_writer = cv2.VideoWriter(
                os.path.join(scenes_folder,scene_filename), fourcc, 30, (frame.shape[1], frame.shape[0]))

        # Write the frame to the scene video file
        if scene_writer is not None:
            scene_writer.write(frame)

        # Update the previous hash and frame count
        prev_hash = curr_hash
        frame_count += 1

    # Release the scene writer and video capture objects
    if scene_writer is not None:
        scene_writer.release()

    video.release()
