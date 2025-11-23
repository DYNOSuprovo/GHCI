# Transaction Categorization System

A robust, explainable, and configurable transaction categorization system.

## Features
- **Configurable Taxonomy**: Define categories in `config/categories.yaml`.
- **Explainable AI**: Uses SHAP to explain predictions.
- **MLOps**: Tracks experiments with MLflow.
- **API & UI**: FastAPI backend and Streamlit frontend.

## Setup

1. Install dependencies:
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

2. Generate data:
```bash
python src/data_generator.py
```

3. Train model:
```bash
python src/model.py
```

4. Run API:
```bash
uvicorn app.main:app --reload
```

5. Run UI:
```bash
streamlit run app/ui.py
```

## Project Structure
- `src/`: Core logic (preprocessing, model, explainability)
- `config/`: Configuration files
- `data/`: Datasets
- `app/`: Application code
- `models/`: Trained models

## Deployment

### Quick Deploy with Docker
```bash
docker-compose up -d
```
Access at: http://localhost:8501

### Cloud Deployment Options
- **Heroku** (Easiest): See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#d-heroku-easiest-for-beginners)
- **GCP Cloud Run**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#a-google-cloud-platform-gcp)
- **AWS**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#b-amazon-web-services-aws)
- **Railway.app**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#e-railwayapp-modern--simple)

For detailed deployment instructions, see **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**
