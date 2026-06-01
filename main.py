import asyncio
import httpx
import os

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("POST_URL")
VIDEO_ID=os.getenv("VIDEO_ID")

TIME = 300 #5 minutes

async def run():
    async with httpx.AsyncClient() as client:
        while True:
            try:
                res = await client.post(URL, json={"video_id": VIDEO_ID})

                print("STATUS:", res.status_code)
                print("BODY:", res.text)

                await asyncio.sleep(TIME)

            except Exception as e:
                print("Error:", e)
                await asyncio.sleep(TIME)

asyncio.run(run())