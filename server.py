from fastapi import FastAPI
from pydantic import BaseModel
from comment import postComment
from youtube import getComments
from pathlib import Path
from dotenv import load_dotenv

load_dotenv();

import json
import os
import httpx


app = FastAPI()


OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")


timeout = httpx.Timeout(120.0)


class ChatRequest(BaseModel):
    video_id: str

@app.post("/post")
async def post(req: ChatRequest):

    Path("db").mkdir(exist_ok=True)
    
    results = []
    video_id = req.video_id;

    Path(f"db/{video_id}").mkdir(parents=True, exist_ok=True)
    
    comments =  getComments(video_id)

    system_prompt = Path("prompts/system.txt").read_text(encoding="utf-8") 

    async with httpx.AsyncClient(timeout=timeout) as client:

        for comment in comments["items"]:

            comment_id = comment["id"]
            comment_text = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comment_path = Path("db") / video_id / f"{comment_id}.json"

            if comment_path.exists():
                print("Reply already posted, moving to the next comment :)")
                results.append({
                    "comment_text": comment_text,
                    "comment_id": comment_id,
                })
                continue
                # theres no new comment, handle replies in future
            else:
                # reply with a new comment
                print(f"""Handling New Comment {comment_text}""")
                
                #
                prompt = f"""
{system_prompt}

Comment:
{comment_text}

Reply:
"""
#
                response = await client.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "prompt": prompt,
                        "stream": False
                    }
                )

                data = response.json()

                if "response" not in data:
                    print("Invalid Ollama response:")
                    print(data)
                    continue
                
                print(data["response"])
                
                postResponse = postComment(comment_id, data["response"])
                print(postResponse)

                comment_response = [comment, postResponse];

                with open(comment_path, "w") as f:
                    json.dump(comment_response, f, indent=2)
                results.append({
                    "comment_id": comment_id,
                    "reply": data["response"]
                })
        return {
            "results": results
        }

@app.get("/get")
async def get():
    # return the comments from the db
    return

@app.get("/test")
async def test():
    return {"status": "ok"}