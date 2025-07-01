from fastapi import APIRouter, Request, Query, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
import sys
import os
import tempfile
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from models.filters import FilterRequest
from services.database import get_filtered_playbyplay
from services.utils import combine_video_clips





# Initialize a FastAPI router (modular way to organize endpoints)
router = APIRouter()


@router.post("/filter_plays")
def filter_plays(filters: FilterRequest):
    """
    Endpoint to filter plays based on provided criteria.
    Accepts POST requests with validated input, calls function from database.py, and returns data as JSON
    
    Parameters:
    - filters (FilterRequest): The filter criteria for querying data.
    
    Returns:
    - List[dict]: A list of dictionaries representing the filtered plays.
    """
    global filtered_data
    filtered_data = {}
    data = get_filtered_playbyplay(filters)
    filtered_data["data"] = data
    return {"status": "success"}


@router.get("/get_filtered_data")
def get_filtered_data():
    """
    Endpoint to retrieve filtered data from the database.
    Accepts POST requests with validated input, calls function from database.py, and returns data as JSON
    
    Parameters:
    - filters (FilterRequest): The filter criteria for querying data.
    
    Returns:
    - List[dict]: A list of dictionaries representing the filtered data.
    """

    return filtered_data.get("data", [])



@router.post("/generate_video")
def generate_video(payload: dict):
    urls = payload.get("urls", [])
    if not urls:
        return JSONResponse(status_code=400, content={"status": "error", "message": "No video URLs provided"})
    
    video_path = combine_video_clips(urls)
    if not video_path:
        return JSONResponse(status_code=500, content={"status": "error", "message": "Failed to generate video"})

    return {"status": "success", "video_path": f"/api/stream_video?filename={os.path.basename(video_path)}"}


def delete_file_after_response(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print("Failed to delete file:", e)

@router.get("/stream_video")
def stream_video(filename: str, background_tasks: BackgroundTasks):
    full_path = os.path.join(tempfile.gettempdir(), filename)
    if os.path.exists(full_path):
        # background_tasks.add_task(delete_file_after_response, full_path)
        return FileResponse(full_path, media_type="video/mp4", filename=filename)
    return JSONResponse(status_code=404, content={"status": "error", "message": "File not found"})


