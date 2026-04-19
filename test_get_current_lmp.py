import asyncio
from backend.services.ercot_client import get_current_lmp
async def run():
    print("Starting...")
    res = await get_current_lmp()
    print(res)
asyncio.run(run())
