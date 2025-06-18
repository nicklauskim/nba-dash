from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class FilterRequest(BaseModel):
    """
    Represents a filter request for querying data, defining a Pydantic model for validating incoming JSON.
    
    Attributes:
        filter (str): The filter condition to apply.
        value (str): The value to use in the filter condition.
    """
    season: Optional[int] = None
    season_type: Optional[int] = None
    player: Optional[List[int]] = None
    team: Optional[str] = None
    opponent: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    action_type: Optional[str] = None
    # sub_type: Optional[str] = None
    # shot_type: Optional[str] = None
    # shot_zone_area: Optional[str] = None


