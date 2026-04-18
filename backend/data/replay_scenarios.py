"""
Multiple historical replay scenarios for various market events.
Each scenario demonstrates Dispatch IQ's value under different conditions.
"""

# ═══════════════════════════════════════════
# SCENARIO 1: Winter Storm Uri — Feb 2021
# Already in uri_replay_data.py (imported separately)
# ═══════════════════════════════════════════

# ═══════════════════════════════════════════
# SCENARIO 2: August 2023 Heat Dome — ERCOT
# Extended 110°F+ heat across Texas, AC load pushes LMP over $5,000
# ═══════════════════════════════════════════
HEAT_DOME_2023_DATA = [
    # Aug 18 — Heat building, normal morning → afternoon spikes
    {"hour": 0, "date": "2023-08-18", "time": "00:00", "lmp": 28.0, "gas_price": 2.65, "temp_f": 88, "regime": "normal"},
    {"hour": 1, "date": "2023-08-18", "time": "01:00", "lmp": 24.0, "gas_price": 2.65, "temp_f": 86, "regime": "normal"},
    {"hour": 2, "date": "2023-08-18", "time": "02:00", "lmp": 22.0, "gas_price": 2.65, "temp_f": 85, "regime": "normal"},
    {"hour": 3, "date": "2023-08-18", "time": "03:00", "lmp": 20.0, "gas_price": 2.65, "temp_f": 84, "regime": "normal"},
    {"hour": 4, "date": "2023-08-18", "time": "04:00", "lmp": 21.0, "gas_price": 2.65, "temp_f": 84, "regime": "normal"},
    {"hour": 5, "date": "2023-08-18", "time": "05:00", "lmp": 25.0, "gas_price": 2.65, "temp_f": 85, "regime": "normal"},
    {"hour": 6, "date": "2023-08-18", "time": "06:00", "lmp": 32.0, "gas_price": 2.68, "temp_f": 88, "regime": "normal"},
    {"hour": 7, "date": "2023-08-18", "time": "07:00", "lmp": 45.0, "gas_price": 2.68, "temp_f": 92, "regime": "normal"},
    {"hour": 8, "date": "2023-08-18", "time": "08:00", "lmp": 58.0, "gas_price": 2.70, "temp_f": 96, "regime": "normal"},
    {"hour": 9, "date": "2023-08-18", "time": "09:00", "lmp": 72.0, "gas_price": 2.70, "temp_f": 99, "regime": "heat_dome"},
    {"hour": 10, "date": "2023-08-18", "time": "10:00", "lmp": 95.0, "gas_price": 2.72, "temp_f": 102, "regime": "heat_dome"},
    {"hour": 11, "date": "2023-08-18", "time": "11:00", "lmp": 130.0, "gas_price": 2.72, "temp_f": 104, "regime": "heat_dome"},
    {"hour": 12, "date": "2023-08-18", "time": "12:00", "lmp": 180.0, "gas_price": 2.75, "temp_f": 106, "regime": "heat_dome"},
    {"hour": 13, "date": "2023-08-18", "time": "13:00", "lmp": 250.0, "gas_price": 2.75, "temp_f": 108, "regime": "heat_dome"},
    {"hour": 14, "date": "2023-08-18", "time": "14:00", "lmp": 420.0, "gas_price": 2.78, "temp_f": 110, "regime": "heat_dome"},
    {"hour": 15, "date": "2023-08-18", "time": "15:00", "lmp": 850.0, "gas_price": 2.80, "temp_f": 112, "regime": "scarcity"},
    {"hour": 16, "date": "2023-08-18", "time": "16:00", "lmp": 2200.0, "gas_price": 2.82, "temp_f": 113, "regime": "scarcity"},
    {"hour": 17, "date": "2023-08-18", "time": "17:00", "lmp": 4500.0, "gas_price": 2.85, "temp_f": 114, "regime": "scarcity"},
    {"hour": 18, "date": "2023-08-18", "time": "18:00", "lmp": 5000.0, "gas_price": 2.88, "temp_f": 112, "regime": "scarcity"},
    {"hour": 19, "date": "2023-08-18", "time": "19:00", "lmp": 3800.0, "gas_price": 2.88, "temp_f": 108, "regime": "scarcity"},
    {"hour": 20, "date": "2023-08-18", "time": "20:00", "lmp": 1500.0, "gas_price": 2.85, "temp_f": 104, "regime": "heat_dome"},
    {"hour": 21, "date": "2023-08-18", "time": "21:00", "lmp": 450.0, "gas_price": 2.82, "temp_f": 100, "regime": "heat_dome"},
    {"hour": 22, "date": "2023-08-18", "time": "22:00", "lmp": 180.0, "gas_price": 2.80, "temp_f": 96, "regime": "heat_dome"},
    {"hour": 23, "date": "2023-08-18", "time": "23:00", "lmp": 85.0, "gas_price": 2.78, "temp_f": 93, "regime": "heat_dome"},

    # Aug 19 — Day 2 even hotter
    {"hour": 24, "date": "2023-08-19", "time": "00:00", "lmp": 55.0, "gas_price": 2.78, "temp_f": 91, "regime": "normal"},
    {"hour": 25, "date": "2023-08-19", "time": "01:00", "lmp": 42.0, "gas_price": 2.78, "temp_f": 89, "regime": "normal"},
    {"hour": 26, "date": "2023-08-19", "time": "02:00", "lmp": 35.0, "gas_price": 2.78, "temp_f": 88, "regime": "normal"},
    {"hour": 27, "date": "2023-08-19", "time": "03:00", "lmp": 30.0, "gas_price": 2.78, "temp_f": 87, "regime": "normal"},
    {"hour": 28, "date": "2023-08-19", "time": "04:00", "lmp": 32.0, "gas_price": 2.78, "temp_f": 87, "regime": "normal"},
    {"hour": 29, "date": "2023-08-19", "time": "05:00", "lmp": 38.0, "gas_price": 2.80, "temp_f": 89, "regime": "normal"},
    {"hour": 30, "date": "2023-08-19", "time": "06:00", "lmp": 52.0, "gas_price": 2.80, "temp_f": 92, "regime": "normal"},
    {"hour": 31, "date": "2023-08-19", "time": "07:00", "lmp": 78.0, "gas_price": 2.82, "temp_f": 96, "regime": "heat_dome"},
    {"hour": 32, "date": "2023-08-19", "time": "08:00", "lmp": 110.0, "gas_price": 2.82, "temp_f": 100, "regime": "heat_dome"},
    {"hour": 33, "date": "2023-08-19", "time": "09:00", "lmp": 160.0, "gas_price": 2.85, "temp_f": 103, "regime": "heat_dome"},
    {"hour": 34, "date": "2023-08-19", "time": "10:00", "lmp": 280.0, "gas_price": 2.85, "temp_f": 106, "regime": "heat_dome"},
    {"hour": 35, "date": "2023-08-19", "time": "11:00", "lmp": 450.0, "gas_price": 2.88, "temp_f": 108, "regime": "heat_dome"},
    {"hour": 36, "date": "2023-08-19", "time": "12:00", "lmp": 680.0, "gas_price": 2.88, "temp_f": 110, "regime": "scarcity"},
    {"hour": 37, "date": "2023-08-19", "time": "13:00", "lmp": 1200.0, "gas_price": 2.90, "temp_f": 112, "regime": "scarcity"},
    {"hour": 38, "date": "2023-08-19", "time": "14:00", "lmp": 2800.0, "gas_price": 2.92, "temp_f": 114, "regime": "scarcity"},
    {"hour": 39, "date": "2023-08-19", "time": "15:00", "lmp": 5000.0, "gas_price": 2.95, "temp_f": 115, "regime": "scarcity"},
    {"hour": 40, "date": "2023-08-19", "time": "16:00", "lmp": 5000.0, "gas_price": 2.95, "temp_f": 116, "regime": "scarcity"},
    {"hour": 41, "date": "2023-08-19", "time": "17:00", "lmp": 5000.0, "gas_price": 2.98, "temp_f": 115, "regime": "scarcity"},
    {"hour": 42, "date": "2023-08-19", "time": "18:00", "lmp": 4200.0, "gas_price": 2.98, "temp_f": 112, "regime": "scarcity"},
    {"hour": 43, "date": "2023-08-19", "time": "19:00", "lmp": 2500.0, "gas_price": 2.95, "temp_f": 108, "regime": "scarcity"},
    {"hour": 44, "date": "2023-08-19", "time": "20:00", "lmp": 800.0, "gas_price": 2.92, "temp_f": 104, "regime": "heat_dome"},
    {"hour": 45, "date": "2023-08-19", "time": "21:00", "lmp": 320.0, "gas_price": 2.90, "temp_f": 100, "regime": "heat_dome"},
    {"hour": 46, "date": "2023-08-19", "time": "22:00", "lmp": 120.0, "gas_price": 2.88, "temp_f": 96, "regime": "heat_dome"},
    {"hour": 47, "date": "2023-08-19", "time": "23:00", "lmp": 65.0, "gas_price": 2.85, "temp_f": 93, "regime": "normal"},
]

# ═══════════════════════════════════════════
# SCENARIO 3: Spring Wind Glut — Apr 2024
# West TX wind corridor overproduction → negative LMP
# Shows when Dispatch IQ says "IMPORT" and saves money
# ═══════════════════════════════════════════
WIND_GLUT_2024_DATA = [
    # Apr 12 — Wind ramping up overnight, prices collapsing
    {"hour": 0, "date": "2024-04-12", "time": "00:00", "lmp": 18.0, "gas_price": 1.80, "temp_f": 68, "regime": "normal"},
    {"hour": 1, "date": "2024-04-12", "time": "01:00", "lmp": 12.0, "gas_price": 1.80, "temp_f": 66, "regime": "normal"},
    {"hour": 2, "date": "2024-04-12", "time": "02:00", "lmp": 5.0, "gas_price": 1.80, "temp_f": 64, "regime": "wind_glut"},
    {"hour": 3, "date": "2024-04-12", "time": "03:00", "lmp": -2.0, "gas_price": 1.80, "temp_f": 63, "regime": "wind_glut"},
    {"hour": 4, "date": "2024-04-12", "time": "04:00", "lmp": -8.0, "gas_price": 1.80, "temp_f": 62, "regime": "wind_glut"},
    {"hour": 5, "date": "2024-04-12", "time": "05:00", "lmp": -15.0, "gas_price": 1.78, "temp_f": 61, "regime": "wind_glut"},
    {"hour": 6, "date": "2024-04-12", "time": "06:00", "lmp": -22.0, "gas_price": 1.78, "temp_f": 60, "regime": "wind_glut"},
    {"hour": 7, "date": "2024-04-12", "time": "07:00", "lmp": -18.0, "gas_price": 1.78, "temp_f": 62, "regime": "wind_glut"},
    {"hour": 8, "date": "2024-04-12", "time": "08:00", "lmp": -10.0, "gas_price": 1.80, "temp_f": 65, "regime": "wind_glut"},
    {"hour": 9, "date": "2024-04-12", "time": "09:00", "lmp": 2.0, "gas_price": 1.80, "temp_f": 68, "regime": "wind_glut"},
    {"hour": 10, "date": "2024-04-12", "time": "10:00", "lmp": 8.0, "gas_price": 1.82, "temp_f": 72, "regime": "oversupply"},
    {"hour": 11, "date": "2024-04-12", "time": "11:00", "lmp": 15.0, "gas_price": 1.82, "temp_f": 75, "regime": "normal"},
    {"hour": 12, "date": "2024-04-12", "time": "12:00", "lmp": 22.0, "gas_price": 1.85, "temp_f": 78, "regime": "normal"},
    {"hour": 13, "date": "2024-04-12", "time": "13:00", "lmp": 28.0, "gas_price": 1.85, "temp_f": 80, "regime": "normal"},
    {"hour": 14, "date": "2024-04-12", "time": "14:00", "lmp": 35.0, "gas_price": 1.88, "temp_f": 82, "regime": "normal"},
    {"hour": 15, "date": "2024-04-12", "time": "15:00", "lmp": 42.0, "gas_price": 1.88, "temp_f": 84, "regime": "normal"},
    {"hour": 16, "date": "2024-04-12", "time": "16:00", "lmp": 48.0, "gas_price": 1.90, "temp_f": 85, "regime": "normal"},
    {"hour": 17, "date": "2024-04-12", "time": "17:00", "lmp": 55.0, "gas_price": 1.90, "temp_f": 84, "regime": "normal"},
    {"hour": 18, "date": "2024-04-12", "time": "18:00", "lmp": 62.0, "gas_price": 1.92, "temp_f": 82, "regime": "normal"},
    {"hour": 19, "date": "2024-04-12", "time": "19:00", "lmp": 48.0, "gas_price": 1.92, "temp_f": 78, "regime": "normal"},
    {"hour": 20, "date": "2024-04-12", "time": "20:00", "lmp": 35.0, "gas_price": 1.90, "temp_f": 74, "regime": "normal"},
    {"hour": 21, "date": "2024-04-12", "time": "21:00", "lmp": 22.0, "gas_price": 1.88, "temp_f": 71, "regime": "normal"},
    {"hour": 22, "date": "2024-04-12", "time": "22:00", "lmp": 10.0, "gas_price": 1.85, "temp_f": 68, "regime": "wind_glut"},
    {"hour": 23, "date": "2024-04-12", "time": "23:00", "lmp": -5.0, "gas_price": 1.82, "temp_f": 66, "regime": "wind_glut"},

    # Apr 13 — Another wind surge overnight
    {"hour": 24, "date": "2024-04-13", "time": "00:00", "lmp": -12.0, "gas_price": 1.80, "temp_f": 64, "regime": "wind_glut"},
    {"hour": 25, "date": "2024-04-13", "time": "01:00", "lmp": -20.0, "gas_price": 1.78, "temp_f": 62, "regime": "wind_glut"},
    {"hour": 26, "date": "2024-04-13", "time": "02:00", "lmp": -28.0, "gas_price": 1.78, "temp_f": 60, "regime": "wind_glut"},
    {"hour": 27, "date": "2024-04-13", "time": "03:00", "lmp": -35.0, "gas_price": 1.75, "temp_f": 59, "regime": "wind_glut"},
    {"hour": 28, "date": "2024-04-13", "time": "04:00", "lmp": -42.0, "gas_price": 1.75, "temp_f": 58, "regime": "wind_glut"},
    {"hour": 29, "date": "2024-04-13", "time": "05:00", "lmp": -38.0, "gas_price": 1.75, "temp_f": 58, "regime": "wind_glut"},
    {"hour": 30, "date": "2024-04-13", "time": "06:00", "lmp": -25.0, "gas_price": 1.78, "temp_f": 60, "regime": "wind_glut"},
    {"hour": 31, "date": "2024-04-13", "time": "07:00", "lmp": -10.0, "gas_price": 1.78, "temp_f": 63, "regime": "wind_glut"},
    {"hour": 32, "date": "2024-04-13", "time": "08:00", "lmp": 5.0, "gas_price": 1.80, "temp_f": 66, "regime": "oversupply"},
    {"hour": 33, "date": "2024-04-13", "time": "09:00", "lmp": 18.0, "gas_price": 1.80, "temp_f": 70, "regime": "normal"},
    {"hour": 34, "date": "2024-04-13", "time": "10:00", "lmp": 25.0, "gas_price": 1.82, "temp_f": 74, "regime": "normal"},
    {"hour": 35, "date": "2024-04-13", "time": "11:00", "lmp": 32.0, "gas_price": 1.82, "temp_f": 77, "regime": "normal"},
    {"hour": 36, "date": "2024-04-13", "time": "12:00", "lmp": 38.0, "gas_price": 1.85, "temp_f": 80, "regime": "normal"},
    {"hour": 37, "date": "2024-04-13", "time": "13:00", "lmp": 45.0, "gas_price": 1.85, "temp_f": 82, "regime": "normal"},
    {"hour": 38, "date": "2024-04-13", "time": "14:00", "lmp": 52.0, "gas_price": 1.88, "temp_f": 84, "regime": "normal"},
    {"hour": 39, "date": "2024-04-13", "time": "15:00", "lmp": 58.0, "gas_price": 1.88, "temp_f": 85, "regime": "normal"},
    {"hour": 40, "date": "2024-04-13", "time": "16:00", "lmp": 65.0, "gas_price": 1.90, "temp_f": 86, "regime": "normal"},
    {"hour": 41, "date": "2024-04-13", "time": "17:00", "lmp": 72.0, "gas_price": 1.90, "temp_f": 85, "regime": "normal"},
    {"hour": 42, "date": "2024-04-13", "time": "18:00", "lmp": 55.0, "gas_price": 1.88, "temp_f": 82, "regime": "normal"},
    {"hour": 43, "date": "2024-04-13", "time": "19:00", "lmp": 38.0, "gas_price": 1.85, "temp_f": 78, "regime": "normal"},
    {"hour": 44, "date": "2024-04-13", "time": "20:00", "lmp": 22.0, "gas_price": 1.82, "temp_f": 74, "regime": "normal"},
    {"hour": 45, "date": "2024-04-13", "time": "21:00", "lmp": 12.0, "gas_price": 1.80, "temp_f": 70, "regime": "oversupply"},
    {"hour": 46, "date": "2024-04-13", "time": "22:00", "lmp": 2.0, "gas_price": 1.78, "temp_f": 67, "regime": "wind_glut"},
    {"hour": 47, "date": "2024-04-13", "time": "23:00", "lmp": -8.0, "gas_price": 1.75, "temp_f": 65, "regime": "wind_glut"},
]


# ═══════════════════════════════════════════
# SCENARIO METADATA & PROCESSING
# ═══════════════════════════════════════════

SCENARIOS = {
    "uri_2021": {
        "id": "uri_2021",
        "name": "Winter Storm Uri",
        "icon": "❄️",
        "period": "February 13-16, 2021",
        "location": "Midland TX (ERCOT West)",
        "description": "Catastrophic freeze collapsed the ERCOT grid. LMP hit the $9,000/MWh cap for 72+ hours. 4.5M customers lost power.",
        "color": "#3B82F6",
        "badge_bg": "#1E3A5F",
    },
    "heat_dome_2023": {
        "id": "heat_dome_2023",
        "name": "August 2023 Heat Dome",
        "icon": "🔥",
        "period": "August 18-19, 2023",
        "location": "Midland TX (ERCOT West)",
        "description": "Record 116°F temps across Texas. AC load pushed reserves to minimum. LMP spiked to $5,000/MWh at peak.",
        "color": "#F97316",
        "badge_bg": "#7C2D12",
    },
    "wind_glut_2024": {
        "id": "wind_glut_2024",
        "name": "Spring Wind Glut",
        "icon": "🌀",
        "period": "April 12-13, 2024",
        "location": "Midland TX (ERCOT West)",
        "description": "Massive overnight wind output drove LMP to -$42/MWh. Generating during negative pricing means paying the grid to take your power.",
        "color": "#06B6D4",
        "badge_bg": "#164E63",
    },
}


def _enrich_replay_data(raw_data, facility_mw=200):
    """Compute spreads, dispatch decisions, and cumulative savings for replay data."""
    heat_rate = 7.5
    om_cost = 3.50
    enriched = []
    cumulative_savings = 0.0

    for entry in raw_data:
        gen_cost = entry["gas_price"] * heat_rate + om_cost
        spread = entry["lmp"] - gen_cost
        should_generate = spread > 0
        hourly_value = spread * facility_mw if should_generate else 0
        # For wind glut: savings = cost avoided by NOT generating during negative spread
        if not should_generate:
            hourly_value = abs(spread) * facility_mw  # Money saved by importing
        cumulative_savings += hourly_value

        enriched.append({
            **entry,
            "gen_cost": round(gen_cost, 2),
            "spread": round(spread, 2),
            "should_generate": should_generate,
            "recommendation": "GENERATE" if should_generate else "IMPORT",
            "hourly_value": round(hourly_value, 2),
            "cumulative_savings": round(cumulative_savings, 2),
        })

    return enriched


def get_scenario_data(scenario_id: str):
    """Return enriched replay data for a given scenario."""
    if scenario_id == "uri_2021":
        from backend.data.uri_replay_data import get_uri_replay_data
        return get_uri_replay_data()
    elif scenario_id == "heat_dome_2023":
        return _enrich_replay_data(HEAT_DOME_2023_DATA)
    elif scenario_id == "wind_glut_2024":
        return _enrich_replay_data(WIND_GLUT_2024_DATA)
    return None


def get_all_scenarios():
    """Return metadata for all available replay scenarios."""
    return list(SCENARIOS.values())
