"""
Market regime definitions for ERCOT dispatch classification.
Six regime states that determine BTM generation economics.
"""

REGIMES = {
    "normal": {
        "id": "normal",
        "name": "Normal Operations",
        "icon": "✅",
        "color": "#6B7280",
        "badge_bg": "#1F2937",
        "description": "Grid operating within normal parameters. Standard day-ahead and real-time price patterns.",
        "dispatch_note": "Follow standard dispatch schedule based on spread forecast.",
        "lmp_threshold_low": 0,
        "lmp_threshold_high": 80,
    },
    "heat_dome": {
        "id": "heat_dome",
        "name": "Heat Dome",
        "icon": "🔥",
        "color": "#F97316",
        "badge_bg": "#7C2D12",
        "description": "Grid demand elevated due to extreme heat. Air conditioning load driving peak consumption.",
        "dispatch_note": "Expect LMP above $80/MWh through evening hours. Recommend sustained generation.",
        "lmp_threshold_low": 80,
        "lmp_threshold_high": 500,
    },
    "wind_glut": {
        "id": "wind_glut",
        "name": "Wind Surplus",
        "icon": "💨",
        "color": "#06B6D4",
        "badge_bg": "#164E63",
        "description": "High wind generation suppressing real-time prices. West Texas wind farms at peak output.",
        "dispatch_note": "LMP may go negative. Consider reducing generation and importing from grid.",
        "lmp_threshold_low": -50,
        "lmp_threshold_high": 15,
    },
    "scarcity": {
        "id": "scarcity",
        "name": "Scarcity Pricing",
        "icon": "⚡",
        "color": "#EF4444",
        "badge_bg": "#7F1D1D",
        "description": "Operating reserves below threshold. ERCOT deploying emergency pricing adders.",
        "dispatch_note": "LMP includes scarcity adders. Maximize generation — every MWh is extremely valuable.",
        "lmp_threshold_low": 500,
        "lmp_threshold_high": 5000,
    },
    "oversupply": {
        "id": "oversupply",
        "name": "Oversupply",
        "icon": "📉",
        "color": "#8B5CF6",
        "badge_bg": "#4C1D95",
        "description": "Low demand period with excess generation capacity. Typically overnight or mild shoulder seasons.",
        "dispatch_note": "Negative or near-zero spreads likely. Import from grid to minimize fuel costs.",
        "lmp_threshold_low": -100,
        "lmp_threshold_high": 10,
    },
    "winter_storm": {
        "id": "winter_storm",
        "name": "Winter Storm",
        "icon": "❄️",
        "color": "#3B82F6",
        "badge_bg": "#1E3A5F",
        "description": "Cold weather event stressing heating demand. Gas supply disruptions possible.",
        "dispatch_note": "Gas prices may spike due to supply constraints. Monitor fuel availability closely.",
        "lmp_threshold_low": 200,
        "lmp_threshold_high": 9001,
    },
    "uri_emergency": {
        "id": "uri_emergency",
        "name": "URI EMERGENCY",
        "icon": "🚨",
        "color": "#FF0000",
        "badge_bg": "#450A0A",
        "description": "CRITICAL: System-wide emergency. Rolling blackouts in effect. LMP at system cap.",
        "dispatch_note": "MAXIMUM GENERATION. Every MWh generated avoids catastrophic grid purchase costs.",
        "lmp_threshold_low": 5000,
        "lmp_threshold_high": 99999,
    },
}

def get_regime(regime_id: str):
    """Return regime definition by ID."""
    return REGIMES.get(regime_id, REGIMES["normal"])

def classify_regime(lmp: float, gas_price: float = None, temp_f: float = None):
    """Classify current market regime based on LMP and contextual signals."""
    if lmp >= 5000:
        return REGIMES["uri_emergency"]
    if lmp >= 500:
        return REGIMES["scarcity"]
    if temp_f is not None and temp_f >= 100 and lmp >= 60:
        return REGIMES["heat_dome"]
    if lmp >= 80:
        return REGIMES["heat_dome"]
    if temp_f is not None and temp_f <= 20 and lmp >= 200:
        return REGIMES["winter_storm"]
    if lmp <= 10:
        if lmp <= 0:
            return REGIMES["wind_glut"]
        return REGIMES["oversupply"]
    return REGIMES["normal"]
