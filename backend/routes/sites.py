"""Sites API routes — site selection analytics."""
from fastapi import APIRouter
from backend.data.sites_data import get_all_sites, get_site_by_id

router = APIRouter(prefix="/api/sites", tags=["sites"])


@router.get("")
def list_sites():
    """Return all 7 candidate sites with spread economics and composite scores."""
    sites = get_all_sites()
    return {
        "sites": sites,
        "analysis_period": "2019-2024",
        "total_sites": len(sites),
        "top_site": sites[0]["label"] if sites else None,
    }


@router.get("/{site_id}")
def get_site_detail(site_id: str):
    """Return detailed analysis for a single candidate site."""
    site = get_site_by_id(site_id)
    if not site:
        return {"error": f"Site '{site_id}' not found"}
    return site
