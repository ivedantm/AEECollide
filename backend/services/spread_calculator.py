"""
Spread calculator and dispatch optimizer.
Core BTM economics: spread = LMP - (gas_price × heat_rate + O&M)
"""
from backend.config import HEAT_RATE, O_AND_M_COST, FACILITY_SIZE_MW


def calculate_gen_cost(gas_price: float, heat_rate: float = HEAT_RATE, om_cost: float = O_AND_M_COST, temp_f: float = None) -> float:
    """Calculate the cost to generate 1 MWh from BTM gas generator, adjusted for ambient thermodynamics."""
    effective_heat_rate = heat_rate
    if temp_f is not None and temp_f > 59.0:
        # Real-world physics: turbine efficiency degrades ~0.15% per degree F above 59F
        effective_heat_rate = heat_rate * (1.0 + ((temp_f - 59.0) * 0.0015))
        
    return gas_price * effective_heat_rate + om_cost


def calculate_spread(lmp: float, gas_price: float, heat_rate: float = HEAT_RATE, om_cost: float = O_AND_M_COST, temp_f: float = None) -> float:
    """Calculate the BTM generation spread (LMP - gen cost) utilizing ambient temperature parameters."""
    gen_cost = calculate_gen_cost(gas_price, heat_rate, om_cost, temp_f)
    return lmp - gen_cost


def dispatch_decision(spread: float) -> dict:
    """Make a dispatch decision based on spread."""
    if spread > 0:
        return {
            "action": "GENERATE",
            "color": "green",
            "icon": "▲",
            "reason": f"Grid price exceeds generation cost by ${spread:.2f}/MWh",
            "hourly_value": round(spread * FACILITY_SIZE_MW, 2),
        }
    else:
        return {
            "action": "IMPORT",
            "color": "red",
            "icon": "▼",
            "reason": f"Grid power is ${abs(spread):.2f}/MWh cheaper than generating",
            "hourly_value": round(abs(spread) * FACILITY_SIZE_MW, 2),
        }


def calculate_schedule_savings(schedule: list) -> dict:
    """
    Calculate savings from optimal dispatch vs always-generate.
    schedule: list of dicts with 'spread' key for each hour.
    """
    total_savings = 0.0
    total_profit = 0.0
    avoided_uneconomic_hours = 0

    for hour_data in schedule:
        spread = hour_data.get("spread", 0)
        if spread < 0:
            # Import saves us the negative spread × facility size
            total_savings += abs(spread) * FACILITY_SIZE_MW
            avoided_uneconomic_hours += 1
        else:
            # Positive spread = profit from generating
            total_profit += spread * FACILITY_SIZE_MW

    return {
        "total_savings": round(total_savings, 2),
        "total_profit": round(total_profit, 2),
        "avoided_uneconomic_hours": avoided_uneconomic_hours,
        "total_hours": len(schedule),
        "generate_hours": len(schedule) - avoided_uneconomic_hours,
    }
