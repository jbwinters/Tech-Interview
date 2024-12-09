from datetime import datetime, timezone
import json
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import Activity, ActivityType


app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_activities():
    try:
        with open("activities.json", "r") as f:
            data = json.load(f)
            # Convert string dates to datetime
            for activity in data:
                activity['start_time'] = datetime.fromisoformat(activity['start_time'])
                if activity.get('end_time'):
                    activity['end_time'] = datetime.fromisoformat(activity['end_time'])
            return data
    except FileNotFoundError:
        return []


def write_activities(data):
    # Convert datetime to ISO format for JSON serialization
    json_data = []
    for activity in data:
        activity_copy = activity.copy()
        activity_copy['start_time'] = activity_copy['start_time'].isoformat()
        if activity_copy.get('end_time'):
            activity_copy['end_time'] = activity_copy['end_time'].isoformat()
        json_data.append(activity_copy)
    
    with open("activities.json", "w") as f:
        json.dump(json_data, f, indent=2)


@app.post("/activities/")
async def create_activity(activity: Activity):
    data = read_activities()
    data.append(activity.dict())
    write_activities(data)
    return activity


@app.put("/activities/{activity_id}/end")
async def end_activity(activity_id: int):
    data = read_activities()
    for activity in data:
        if activity['id'] == activity_id:
            activity['end_time'] = datetime.now(timezone.utc)
            activity['status'] = 'completed'
            write_activities(data)
            return activity
    raise HTTPException(status_code=404, detail="Activity not found")

# TODO: Implement GET endpoint with filtering
