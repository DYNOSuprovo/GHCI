from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from src.model import TransactionClassifier
from src.explainability import Explainer
from src.data_generator import load_config

app = FastAPI(title="Transaction Categorization API")

# Global models
classifier = TransactionClassifier()
explainer = None
config = load_config()

@app.on_event("startup")
def load_models():
    global classifier, explainer
    model_path = "models/model.pkl"
    if os.path.exists(model_path):
        classifier.load_model(model_path)
        explainer = Explainer(model_path)
    else:
        print("Model not found. Please train the model first.")

class TransactionRequest(BaseModel):
    description: str
    amount: Optional[float] = None

class PredictionResponse(BaseModel):
    category: str
    confidence: float
    explanation: List[dict]

@app.post("/predict", response_model=PredictionResponse)
def predict(request: TransactionRequest):
    if not classifier:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    result = classifier.predict(request.description)[0]
    
    explanation = []
    if explainer:
        explanation = explainer.explain(request.description)
        # Limit to top 5 features
        explanation = explanation[:5]
        
    return {
        "category": result["category"],
        "confidence": result["confidence"],
        "explanation": explanation
    }

class BatchTransactionRequest(BaseModel):
    transactions: List[TransactionRequest]

@app.post("/predict_batch")
def predict_batch(request: BatchTransactionRequest):
    if not classifier:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    results = []
    for txn in request.transactions:
        # For batch, we skip explanation to be faster, or we could make it optional
        # Here we'll skip it for performance
        pred = classifier.predict(txn.description)[0]
        results.append({
            "description": txn.description,
            "amount": txn.amount,
            "category": pred["category"],
            "confidence": pred["confidence"]
        })
        
    return results

class FeedbackRequest(BaseModel):
    description: str
    correct_category: str

@app.post("/feedback")
def submit_feedback(request: FeedbackRequest):
    feedback_file = "data/feedback.csv"
    file_exists = os.path.exists(feedback_file)
    
    with open(feedback_file, "a") as f:
        if not file_exists:
            f.write("description,correct_category\n")
        f.write(f"{request.description},{request.correct_category}\n")
    
    return {"message": "Feedback received"}

@app.get("/categories")
def get_categories():
    return config["categories"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

