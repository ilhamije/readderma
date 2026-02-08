from fastapi import FastAPI, Request, UploadFile, File, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import uuid
import asyncio
import time
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from services import predict_skin_condition, get_real_trials, get_mock_trials, load_ai_model

load_dotenv()

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # Load model on startup
    print("Startup: Initializing AI model...")
    load_ai_model()
    yield
    print("Shutdown: Cleanup.")

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for results (No DB as per constraints)
# Key: task_id, Value: dict with status and result
# In a real app, use Redis or DB.
tasks_db = {}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

def process_analysis(task_id: str, image_bytes: bytes):
    """Background task to process image and fetch trials (Sync for threadpool execution)"""
    try:
        # 1. AI Analysis
        # Simulating a slight delay to make the skeleton loader visible and meaningful
        # Remove sleep in production if strictly speed-focused, but good for UX demo
        time.sleep(1.5) 
        
        ai_result = predict_skin_condition(image_bytes)
        
        trials_data = []
        
        # 2. Fetch trials for the identified condition
        # We fetch trials if the AI identified a condition
        if ai_result.get("condition"):
            trials_data = get_real_trials(ai_result["condition"])
        
        # 3. Store Result
        tasks_db[task_id] = {
            "status": "completed",
            "data": {
                "condition": ai_result["condition"],
                "confidence": ai_result["confidence"],
                "explanation": ai_result["explanation"],
                "trials": trials_data
            }
        }
    except Exception as e:
        print(f"Task Error: {e}")
        tasks_db[task_id] = {
            "status": "error",
            "error": str(e)
        }

@app.post("/analyze")
async def analyze_skin(request: Request, background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Generate unique ID
    task_id = str(uuid.uuid4())
    
    # Read file content immediately
    contents = await file.read()
    
    # Set initial status
    tasks_db[task_id] = {"status": "processing"}
    
    # Add to background tasks
    background_tasks.add_task(process_analysis, task_id, contents)
    
    # Redirect to processing page
    return RedirectResponse(url=f"/processing/{task_id}", status_code=303)

@app.get("/processing/{task_id}", response_class=HTMLResponse)
async def processing_page(request: Request, task_id: str):
    if task_id not in tasks_db:
        return RedirectResponse(url="/")
        
    return templates.TemplateResponse("processing.html", {"request": request, "task_id": task_id})

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    task = tasks_db.get(task_id)
    if not task:
        return JSONResponse({"status": "not_found"}, status_code=404)
    return JSONResponse(task)

@app.get("/result/{task_id}", response_class=HTMLResponse)
async def result_page(request: Request, task_id: str):
    task = tasks_db.get(task_id)
    if not task or task.get("status") != "completed":
        return RedirectResponse(url=f"/processing/{task_id}")
    
    data = task["data"]
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "condition": data["condition"],
        "confidence": data["confidence"],
        "explanation": data["explanation"],
        "trials": data["trials"]
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
