from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pymongo import MongoClient
import os

# ---- Database Setup ----
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI environment variable is not set. Configure it in Render dashboard or a .env file.")
client = MongoClient(MONGO_URI)
db = client["healthdb"]
collection = db["health_data"]

# ---- Pydantic Model ----
class HealthDataModel(BaseModel):
    timestamp: str

    heartRate: Optional[float] = None
    restingHeartRate: Optional[float] = None
    heartRateVariabilitySDNN: Optional[float] = None
    oxygenSaturation: Optional[float] = None
    respiratoryRate: Optional[float] = None
    bodyTemperature: Optional[float] = None
    irregularHeartRhythmEvent: Optional[int] = None
    highHeartRateEvent: Optional[int] = None
    lowHeartRateEvent: Optional[int] = None
    ecgClassification: Optional[str] = None
    ecgAverageHeartRate: Optional[float] = None
    sleepAnalysisValue: Optional[int] = None
    appleSleepingWristTemperature: Optional[float] = None
    numberOfTimesFallen: Optional[float] = None
    atrialFibrillationBurden: Optional[float] = None
    bloodPressureSystolic: Optional[float] = None
    bloodPressureDiastolic: Optional[float] = None
    appleWalkingSteadiness: Optional[float] = None
    appleWalkingSteadinessEvent: Optional[int] = None
    forcedExpiratoryVolume1: Optional[float] = None
    forcedVitalCapacity: Optional[float] = None
    peakExpiratoryFlowRate: Optional[float] = None
    bloodGlucose: Optional[float] = None
    insulinDelivery: Optional[float] = None

    device: Optional[str] = None

# ---- FastAPI App ----
app = FastAPI(title="Health Data API")

@app.get("/")
def root():
    return {"status": "ok", "message": "Health Data API running"}

@app.post("/healthdata")
def create_healthdata(data: HealthDataModel):
    doc = data.dict()
    # Parse timestamp to ensure valid ISO8601
    try:
        datetime.fromisoformat(doc["timestamp"].replace("Z", "+00:00"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid timestamp format. Use ISO8601.")

    result = collection.insert_one(doc)
    return {"id": str(result.inserted_id), "message": "Health data stored successfully"}

@app.get("/healthdata")
def get_healthdata(limit: int = 10):
    docs = list(collection.find().sort("timestamp", -1).limit(limit))
    for d in docs:
        d["_id"] = str(d["_id"])
    return docs