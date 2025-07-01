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
    print("Combining the following clips:")
    for i, url in enumerate(urls):
        try:
            print(" -", url)
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(r.content)
                    tmp.flush()
                    clips.append(VideoFileClip(tmp.name))
        except Exception as e:
            print(f"Error loading clip: {url} => {e}")

    if not clips:
        return None

    print(f"Loaded {len(clips)} clips successfully.")
    final = concatenate_videoclips(clips, method="compose")
    print("Video clips combined successfully.")
    out_path = os.path.join(tempfile.gettempdir(), "combined_output.mp4")
    final.write_videofile(out_path, codec="libx264", audio_codec="aac", fps=24, audio=True, logger=None)
    print("Final video written to:", out_path)
    return out_path