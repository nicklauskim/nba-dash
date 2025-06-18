# Useful miscellaneous helper functions

from moviepy import VideoFileClip, concatenate_videoclips
import tempfile
import requests
import os


def rename_columns(api_col_names):
    rename_dict = {}
    for name in api_col_names:
        rename_dict[name] = name.lower()
    return rename_dict


def clean_timestamp(time_string):
    return time_string[:-9]


def combine_video_clips(urls):
    """
    Combines multiple video clips into one.

    Args:
        urls (list): List of video URLs to combine.
    Returns:
        str: Path to the combined video file.
    """
    clips = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                temp_file.write(response.content)
                clips.append(VideoFileClip(temp_file.name))
        
    final_clip = concatenate_videoclips(clips, method="compose")