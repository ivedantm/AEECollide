import os
import json

SITES = [
    {
        "id": "midland",
        "rank": 1,
        "name": "Midland",
        "state": "TX",
        "label": "Midland TX",
        "lat": 31.9973,
        "lng": -102.0779,
        "zone": "ERCOT West",
        "settlement_point": "LZ_WEST",
        "gas_hub": "Waha",
        "insight": "Midland benefits from Waha basis discounts and sits in ERCOT's West zone.",
    },
    {
        "id": "houston",
        "rank": 2,
        "name": "Houston",
        "state": "TX",
        "label": "Houston TX",
        "lat": 29.7604,
        "lng": -95.3698,
        "zone": "ERCOT Houston",
        "settlement_point": "LZ_HOUSTON",
        "gas_hub": "Katy",
        "insight": "Houston faces immense summer cooling loads and volatile coastal weather, resulting in massive peak spreads.",
    },
    {
        "id": "odessa",
        "rank": 3,
        "name": "Odessa",
        "state": "TX",
        "label": "Odessa TX",
        "lat": 31.8457,
        "lng": -102.3676,
        "zone": "ERCOT West",
        "settlement_point": "LZ_WEST",
        "gas_hub": "Waha",
        "insight": "Odessa shares Midland's Waha gas advantage with high reliability.",
    },
    {
        "id": "abilene",
        "rank": 4,
        "name": "Abilene",
        "state": "TX",
        "label": "Abilene TX",
        "lat": 32.4487,
        "lng": -99.7331,
        "zone": "ERCOT West",
        "settlement_point": "LZ_WEST",
        "gas_hub": "Waha",
        "insight": "Abilene sits at the eastern edge of the West zone with high wind exposure.",
    },
    {
        "id": "dallas",
        "rank": 5,
        "name": "Dallas",
        "state": "TX",
        "label": "Dallas TX",
        "lat": 32.7767,
        "lng": -96.7970,
        "zone": "ERCOT North",
        "settlement_point": "LZ_NORTH",
        "gas_hub": "Katy",
        "insight": "Dallas acts as the major load center for North Texas with relatively stable pricing.",
    },
    {
        "id": "san_antonio",
        "rank": 6,
        "name": "San Antonio",
        "state": "TX",
        "label": "San Antonio TX",
        "lat": 29.4241,
        "lng": -98.4936,
        "zone": "ERCOT South",
        "settlement_point": "LZ_SOUTH",
        "gas_hub": "Katy",
        "insight": "San Antonio borders wind-heavy South Texas but faces rapid population growth demand.",
    },
    {
        "id": "chandler",
        "rank": 7,
        "name": "Chandler",
        "state": "AZ",
        "label": "Chandler AZ",
        "lat": 33.3062,
        "lng": -111.8413,
        "zone": "WECC Southwest",
        "settlement_point": "PALOVRDE_ASR-APND",
        "gas_hub": "SoCal Border",
        "insight": "Chandler utilizes the massive Palo Verde hub serving major Arizona data center clusters.",
    },
    {
        "id": "tucson",
        "rank": 8,
        "name": "Tucson",
        "state": "AZ",
        "label": "Tucson AZ",
        "lat": 32.2226,
        "lng": -110.9747,
        "zone": "WECC Southwest",
        "settlement_point": "PALOVRDE_ASR-APND",
        "gas_hub": "SoCal Border",
        "insight": "Tucson tracks Palo Verde with high volatility during evening peak ramps.",
    },
    {
        "id": "las_vegas",
        "rank": 9,
        "name": "Las Vegas",
        "state": "NV",
        "label": "Las Vegas NV",
        "lat": 36.1716,
        "lng": -115.1391,
        "zone": "WECC Mead",
        "settlement_point": "PALOVRDE_ASR-APND",
        "gas_hub": "SoCal Border",
        "insight": "Las Vegas connects through the Mead interchange to Palo Verde, tracking Southwest desert pricing.",
    },
    {
        "id": "los_lunas",
        "rank": 10,
        "name": "Los Lunas",
        "state": "NM",
        "label": "Los Lunas NM",
        "lat": 34.8062,
        "lng": -106.7299,
        "zone": "WECC Southwest",
        "settlement_point": "PALOVRDE_ASR-APND",
        "gas_hub": "SoCal Border",
        "insight": "Los Lunas represents the rising New Mexico data center corridor connected via WECC lines.",
    },
    {
        "id": "rio_rancho",
        "rank": 11,
        "name": "Rio Rancho",
        "state": "NM",
        "label": "Rio Rancho NM",
        "lat": 35.2328,
        "lng": -106.6630,
        "zone": "WECC Southwest",
        "settlement_point": "PALOVRDE_ASR-APND",
        "gas_hub": "SoCal Border",
        "insight": "Rio Rancho serves major technology hubs tracking the greater Southwest power dynamics.",
    },
    {
        "id": "los_angeles",
        "rank": 12,
        "name": "Los Angeles",
        "state": "CA",
        "label": "Los Angeles CA",
        "lat": 34.0522,
        "lng": -118.2437,
        "zone": "CAISO SP15",
        "settlement_point": "TH_SP15_GEN-APND",
        "gas_hub": "SoCal Citygate",
        "insight": "Los Angeles benefits from SP15 Hub liquidity but faces high SoCal gas costs.",
    },
    {
        "id": "bakersfield",
        "rank": 13,
        "name": "Bakersfield",
        "state": "CA",
        "label": "Bakersfield CA",
        "lat": 35.3733,
        "lng": -119.0187,
        "zone": "CAISO ZP26",
        "settlement_point": "TH_ZP26_GEN-APND",
        "gas_hub": "Kern River",
        "insight": "Bakersfield (ZP26) is a solar-heavy zone with frequent afternoon oversupply.",
    }
]

# ── Overlay Real Metrics from site_rankings.json ──
RANKINGS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "site_rankings.json")
if os.path.exists(RANKINGS_PATH):
    try:
        with open(RANKINGS_PATH, "r") as f:
            rankings = json.load(f)
            for site in SITES:
                real_data = rankings.get(site["id"])
                if real_data:
                    site.update({
                        "rank": real_data.get("rank", site.get("rank")),
                        "avg_spread": real_data.get("avg_spread", site.get("avg_spread")),
                        "positive_hours_pct": real_data.get("positive_hours_pct", site.get("positive_hours_pct")),
                        "volatility": real_data.get("volatility", site.get("volatility")),
                        "composite_score": real_data.get("composite_score", site.get("composite_score")),
                        "monthly_spreads": real_data.get("monthly_spreads", []),
                        "regime_breakdown": real_data.get("regime_breakdown", {}),
                        "insight": f"REAL DATA VERSION: {site.get('insight', '')}"
                    })
    except Exception as e:
        print(f"⚠️ Failed to load real site rankings: {e}")

def get_all_sites():
    return sorted(SITES, key=lambda s: s.get("composite_score", 0), reverse=True)

def get_site_by_id(site_id: str):
    for site in SITES:
        if site["id"] == site_id:
            return site
    return None
