from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class ActivityType(str, Enum):
    """Type of work activity performed in the greenhouse.
    
    Supported activities:
    - TRANSPLANTING: Moving plants to new growing locations
    - HARVESTING: Collecting mature crops
    - WEIGHING: Recording crop weights at stations
    - MAINTENANCE: Equipment or facility upkeep
    """

    TRANSPLANTING = "transplanting"
    HARVESTING = "harvesting"
    WEIGHING = "weighing"
    MAINTENANCE = "maintenance"


class ActivityStatus(str, Enum):
    """Status of a work activity.
    
    Values:
    - ACTIVE: Activity is currently in progress
    - COMPLETED: Activity has been finished
    """
    ACTIVE = "active"
    COMPLETED = "completed"


class GrowLocation(BaseModel):
    """Represents a location within a greenhouse facility.
    
    A growing location is specified by hierarchical coordinates:
    - site: The greenhouse facility (e.g., "greenhouse-1")
    - zone: A section within the site (e.g., "A", "B", "C")
    - row: An optional row number within the zone (e.g., "12")
    - channel: An optional channel number within the row (e.g., "3")
    
    Example:
        {
            "site": "greenhouse-1",
            "zone": "A", 
            "row": 12,
            "channel": 3
        }
    
    Note that row and channel are optional to support activities that:
    - Occur across an entire zone
    - Happen in non-growing areas (e.g., packing stations)
    """

    site: str
    zone: str
    row: Optional[int]
    channel: Optional[int]


class Activity(BaseModel):
    """Tracks a discrete work activity performed by one or more workers.

    An activity represents a specific task being performed at a location by workers.
    Activities have a defined start time and an optional end time. They can be 
    performed by individuals or teams, with optional team leadership.

    Attributes:
        id: Unique identifier for the activity
        type: The kind of work being performed (see ActivityType)
        location: Where the activity is taking place
        start_time: When the activity began
        end_time: When the activity finished (None if ongoing)
        worker_ids: List of worker IDs performing the activity
        team_lead_id: Optional ID of the worker leading the team
        status: Current state of the activity (e.g., "active", "completed")
        metadata: Additional activity-specific data (e.g., equipment used, crop type)
    """

    id: int
    type: ActivityType
    location: GrowLocation
    start_time: datetime
    end_time: Optional[datetime]
    worker_ids: List[str]
    team_lead_id: Optional[str]
    status: ActivityStatus
    metadata: Dict  # Flexible field for activity-specific data

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: Optional[datetime], values: dict) -> Optional[datetime]:
        end_time = v
        if end_time \
            and values.data.get("start_time") \
            and end_time > values.data["start_time"]:
                raise ValueError("end_time must be after start_time")
        return end_time

