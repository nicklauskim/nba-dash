from fastapi import APIRouter
import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from models.filters import FilterRequest
from services.database import get_filtered_playbyplay





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