import asyncio
import httpx
import os
import traceback

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("POST_URL")
VIDEO_ID=os.getenv("VIDEO_ID")

TIME = 300 #5 minutes

async def run():
    async with httpx.AsyncClient(timeout=120) as client:
        while True:
            try:
                print("Checking Recent Comments:")
                res = await client.post(URL, json={"video_id": VIDEO_ID})

                print("STATUS:", res.status_code)
                print("BODY:", res.text)

                print("sleeping...")

                await asyncio.sleep(TIME)

            except Exception:
                traceback.print_exc()
                await asyncio.sleep(TIME)

asyncio.run(run())