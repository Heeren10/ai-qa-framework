import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from agent import BusinessAnalystAgent

load_dotenv()

app = FastAPI(title="AI QA Framework - Logic Alignment")

# Check API key on startup
if not os.getenv("GEMINI_API_KEY"):
    print("WARNING: GEMINI_API_KEY is not set in the environment.")

app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    url: str
    brd: str

@app.post("/api/analyze")
async def analyze_logic(request: AnalyzeRequest):
    agent = BusinessAnalystAgent()
    try:
        result = agent.analyze(request.url, request.brd)
        return {"status": "success", "data": result}
    except Exception as e:
        print("❌ ERROR:", str(e))   # <-- ADD THIS
        raise HTTPException(status_code=500, detail=str(e))
