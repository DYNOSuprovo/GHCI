- **Autonomous**: Runs entirely locally or in a container (no external APIs).
- **Explainable**: Tells you *why* a transaction was categorized a certain way.
- **Adaptable**: Users can correct mistakes, and the system learns from them.

### 📄 Documentation
For a deep dive into the system architecture and design, please refer to the project report:
👉 **[AI-Driven Transaction Categorization System.pdf](AI-Driven%20Transaction%20Categorization%20System.pdf)**

---

## 🛠️ Tech Stack & Workflow

### Architecture
The system follows a microservices-like architecture (even when running monolithically):

1.  **Data Ingestion**: Synthetic data generation (`src/data_generator.py`) simulates real-world banking transactions with noise.
2.  **Preprocessing**: Text normalization (`src/preprocessing.py`) cleans raw strings (removes special chars, lowercases).
3.  **Model Training**: A TF-IDF + Logistic Regression pipeline (`src/model.py`) trains on the data.
4.  **Inference API**: FastAPI (`app/main.py`) serves the model and handles batch requests.
5.  **User Interface**: Streamlit (`app/ui.py`) provides an interactive dashboard for users.
6.  **Feedback Loop**: User corrections are saved to `data/feedback.csv` for future retraining.

### Libraries Used
- **Machine Learning**: `scikit-learn`, `pandas`, `numpy`
- **Explainability**: `shap` (SHapley Additive exPlanations)
- **Backend**: `fastapi`, `uvicorn`
- **Frontend**: `streamlit`
- **Ops**: `docker`, `mlflow` (experiment tracking)

---

## � File Structure & Details

| File/Directory | Description |
|----------------|-------------|
| `app/main.py` | **FastAPI Backend**: Handles `/predict`, `/predict_batch`, and `/feedback` endpoints. |
| `app/ui.py` | **Streamlit Frontend**: The UI that connects to the FastAPI backend. |
| `app/streamlit_app.py` | **Standalone App**: A self-contained version for Streamlit Cloud deployment (Monolith). |
| `src/model.py` | **Model Logic**: Defines `TransactionClassifier` class, training loop, and evaluation metrics. |
| `src/data_generator.py` | **Data Engine**: Generates 50,000+ synthetic transactions based on `categories.yaml`. |
| `src/explainability.py` | **XAI Engine**: Generates SHAP values to explain model predictions. |
| `config/categories.yaml` | **Configuration**: Defines the taxonomy (Categories and Keywords). |
| `Dockerfile` | **Deployment**: Defines the container environment for Render/Docker. |
| `requirements.txt` | **Dependencies**: List of Python packages required. |

---

## 🚀 How to Run

### Option 1: Live Demo (Easiest)
Simply visit the [Live App](https://dynosuprovo-ghci-appstreamlit-app-okqqdx.streamlit.app/).

### Option 2: Run Locally (Docker)
If you have Docker installed:
```bash
docker-compose up -d
```
- UI: `http://localhost:8501`
- API: `http://localhost:8000/docs`

### Option 3: Run Locally (Python)
1. **Clone & Install**:
   ```bash
   git clone https://github.com/DYNOSuprovo/GHCI.git
   cd GHCI
   python -m venv venv
   .\venv\Scripts\activate  # or source venv/bin/activate on Mac/Linux
   pip install -r requirements.txt
   ```

2. **Train Model**:
   ```bash
   python src/data_generator.py  # Generate data
   python src/model.py           # Train model
   ```

3. **Run App**:
   ```bash
   streamlit run app/streamlit_app.py
   ```

---

## 🧠 Key Functions Explained

### `TransactionClassifier.train()`
- Loads data from CSV.
- Splits into Train/Test sets.
- Trains a `TfidfVectorizer` + `LogisticRegression` pipeline.
- Logs metrics (Accuracy, F1-Score) to MLflow.
- Generates and saves a Confusion Matrix.

### `Explainer.explain(text)`
- Uses a SHAP KernelExplainer.
- Calculates the contribution of each word to the final prediction.
- Returns a list of `{word, contribution}` for visualization.

### `predict_batch(transactions)`
- Optimized endpoint for processing thousands of transactions at once.
- Skips SHAP generation for speed.
- Returns a JSON list of categories and confidence scores.

---

## 🤝 Contributing
1. Fork the repo.
2. Create a branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Added feature"`
4. Push: `git push origin feature-name`
5. Open a Pull Request!

---

## 📄 License
MIT License. Free to use and modify.
