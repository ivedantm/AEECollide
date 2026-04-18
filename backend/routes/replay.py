"""Replay API routes — multiple historical scenario replays."""
from fastapi import APIRouter
from backend.data.uri_replay_data import get_uri_replay_data
from backend.data.replay_scenarios import get_scenario_data, get_all_scenarios, SCENARIOS

router = APIRouter(prefix="/api/replay", tags=["replay"])


@router.get("/scenarios")
def list_scenarios():
    """Return all available replay scenarios with metadata."""
    return {"scenarios": get_all_scenarios()}


@router.get("/uri")
def get_uri_replay():
    """Legacy endpoint — returns Winter Storm Uri replay."""
    data = get_uri_replay_data()
    return {
        "event": "Winter Storm Uri",
        "period": "February 13-16, 2021",
        "facility_mw": 200,
        "total_hours": len(data),
        "total_savings": data[-1]["cumulative_savings"] if data else 0,
        "data": data,
    }


@router.get("/{scenario_id}")
def get_scenario_replay(scenario_id: str):
    """
    Return a full replay dataset for any scenario.
    scenario_id: 'uri_2021', 'heat_dome_2023', 'wind_glut_2024'
    """
    data = get_scenario_data(scenario_id)
    if data is None:
        return {"error": f"Unknown scenario: {scenario_id}"}

    meta = SCENARIOS.get(scenario_id, {})

    return {
        "event": meta.get("name", scenario_id),
        "period": meta.get("period", ""),
        "location": meta.get("location", ""),
        "description": meta.get("description", ""),
        "icon": meta.get("icon", ""),
        "color": meta.get("color", "#6B7280"),
        "facility_mw": 200,
        "total_hours": len(data),
        "total_savings": data[-1]["cumulative_savings"] if data else 0,
        "data": data,
    }
