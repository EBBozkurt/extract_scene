import cv2
import imagehash
from PIL import Image
import os

from .file_services import get_video_name_from_given_path

# Global video scenes variable to store video names temporary for the excel
video_scenes = []


def get_video_scenes():
    # Returns global "video_scenes" variable for the external usage.
    return video_scenes


def extract_scenes(video_path: str, scene_threshold: int):
    """
    Extracts scenes from a video based on a specified threshold.

    Args:
        video_path (str): Path to the video file.
        scene_threshold (int): Threshold for scene change detection.

    Returns:
        None
    """

    # Decleration of global video_scenes variable
    global video_scenes

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

    # Get video name without its extension
    video_name = get_video_name_from_given_path(video_path)

    # Define the output video file name
    scene_filename = f"{video_name}_scene_{scene_count}.mp4"

    # Add scene_filename to the global video_scenes list
    video_scenes.append(scene_filename[:scene_filename.rfind(".")])

    # Create a directory for the scenes extracted.
    scenes_folder = f"extracted_scenes/{video_name}_scenes"

    # Create a directory for the scenes
    os.makedirs(scenes_folder)

    # Initialize video writer for the first scene
    scene_writer = cv2.VideoWriter(
        os.path.join(scenes_folder, scene_filename), fourcc, 30, (prev_frame.shape[1], prev_frame.shape[0]))

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
            print(f"Scene change detected at {video_name} frame {frame_count}")

            # Release the previous scene writer
            scene_writer.release()

            # Initialize the scene writer
            scene_writer = cv2.VideoWriter(
                os.path.join(scenes_folder, scene_filename), fourcc, 30, (frame.shape[1], frame.shape[0]))

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

    # Decleration of global video_scenes variable
    global video_scenes

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
    print(
        f"Video {video_name} Scene {scene_count} starts at frame {frame_count}")

    # Get video name without its extension
    video_name = get_video_name_from_given_path(video_path)

    # Define the output video file name
    scene_filename = f"{video_name}_scene_{scene_count}.mp4"
    # Add scene_filename to the global video_scenes list
    video_scenes.append(scene_filename[:scene_filename.rfind(".")])

    # Create a directory for the scenes extracted.
    scenes_folder = f"extracted_scenes/{video_name}_scenes"
    master_folder = "extracted_scenes"

    # Create a directory for the scenes
    os.makedirs(scenes_folder)

    # Initialize the scene writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    scene_writer = cv2.VideoWriter(
        os.path.join(scenes_folder, scene_filename), fourcc, 30, (prev_frame.shape[1], prev_frame.shape[0]))
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
            print(f"{video_name} Scene {scene_count} starts at frame {frame_count}")

            if scene_writer is not None:
                # Release the previous scene writer
                scene_writer.release()

            # Define the output video file name
            scene_filename = f"{video_name}_scene_{scene_count}.mp4"

            # Add scene_filename to the global video_scenes list
            video_scenes.append(scene_filename[:scene_filename.rfind(".")])

            # Initialize the scene writer
            scene_writer = cv2.VideoWriter(
                os.path.join(scenes_folder, scene_filename), fourcc, 30, (frame.shape[1], frame.shape[0]))

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


def get_video_name_from_given_path(video_path) -> str:
    """
    Returns the video name from the full path
    """
    # Extracts the file name from the path
    video_name = os.path.basename(video_path)

    video_name_without_extension = os.path.splitext(
        video_name)[0]  # Removes the file extension

    return video_name_without_extension

def extract_scenes2(video_path: str, threshold: int):
    """
    Extracts scenes from a video based on average hash algorithm.

    Args:
        video_path (str): Path to the video file.
        threshold (int): Threshold for scene change detection.

    Returns:
        None
    """    
    # Decleration of global video_scenes variable
    global video_scenes

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

    # Get video name without its extension
    video_name = get_video_name_from_given_path(video_path)

    # Define the output video file name
    scene_filename = f"{video_name}_scene_{scene_count}.mp4"

    # Add scene_filename to the global video_scenes list
    video_scenes.append(scene_filename[:scene_filename.rfind(".")])    
    
    # Create a directory for the scenes extracted.
    scenes_folder = f"extracted_scenes/{video_name}_scenes"

    # Create a directory for the scenes
    os.makedirs(scenes_folder)

    # Initialize the scene writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    scene_writer = cv2.VideoWriter(
        os.path.join(scenes_folder, scene_filename), fourcc, 30, (prev_frame.shape[1], prev_frame.shape[0]))
    scene_writer.write(prev_frame)
    
    print(f"{video_name} Scene {scene_count} extracted")    
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

            # If frame count greater than 30, extract the scene.
            if frame_count >= 30:
                scene_count += 1

                # Define the output video file name
                scene_filename = f"{video_name}_scene_{scene_count}.mp4"

                # Add scene_filename to the global video_scenes list
                video_scenes.append(scene_filename[:scene_filename.rfind(".")])
                print(f"{video_name} Scene {scene_count} extracted") 
                

                       

                if scene_writer is not None:
                    # Release the previous scene writer
                    scene_writer.release()

                # Reset the frame_count variable for the further scenes
                frame_count = 0

                # Initialize the scene writer
                scene_writer = cv2.VideoWriter(
                    os.path.join(scenes_folder, scene_filename), fourcc, 30, (frame.shape[1], frame.shape[0]))
            

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


