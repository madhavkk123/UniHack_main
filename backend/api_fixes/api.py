from fastapi import FastAPI, HTTPException, Request
import uvicorn
import json
from read_data import read_json_file, askQuestion
from scrape import scrape_subject_page
from arjun import get_subject_page_url

# Initialize FastAPI app
app = FastAPI(
    title="Study Assistant API",
    description="API for querying study materials and getting AI-generated answers",
    version="1.0.0"
)

# Load data at startup
# Commented out to avoid startup errors
study_data = {}  # Initialize as empty dict instead of None

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the Study Assistant API"}

@app.post("/get_subject_context")
async def get_subject_context(request: Request):
    """
    Get the context for a subject.
    
    Request body should contain:
    - query: The question to ask
    """
    try:
        body = await request.json()
        query = body.get("query")
        
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")
            
        subject_page_urls = get_subject_page_url(query)
        
        if not subject_page_urls:
            return {"message": "No results found for the query", "data": []}
            
        # If we get a list of URLs, use the first one
        if isinstance(subject_page_urls, list):
            if len(subject_page_urls) > 0:
                subject_page_url = subject_page_urls[0]
                subject_page_data = scrape_subject_page(subject_page_url)
                return {"data": json.loads(subject_page_data), "all_urls": subject_page_urls}
            else:
                return {"message": "No results found for the query", "data": []}
        else:
            # If it's a single URL
            subject_page_data = scrape_subject_page(subject_page_urls)
            return {"data": json.loads(subject_page_data)}
            
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/ask")
async def ask_question(request: Request):
    """
    Ask a question about the study materials.
    
    Request body should contain:
    - query: The question to ask
    - conversation_history: Optional list of previous Q&A exchanges
    - study_data: The subject to ask the question about for the context as a string
    """
    try:
        body = await request.json()
        query = body.get("query")
        conversation_history = body.get("conversation_history", [])
        #subject = body.get("subject")
        study_data = body.get("study_data")
        if not query:
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        answer_text = askQuestion(study_data, query, conversation_history)
        return {"answer": answer_text}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "data_loaded": bool(study_data)}

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 