# 💰 Transaction Categorization System

A robust, explainable, and production-ready AI system for categorizing financial transactions. Built with **FastAPI**, **Streamlit**, and **Scikit-learn**, it features explainable AI (SHAP), batch processing, and a human-in-the-loop feedback mechanism.

---

## 🚀 Live Demo
**Frontend**: [Streamlit App](https://dynosuprovo-ghci-appstreamlit-app-okqqdx.streamlit.app/)  
**Backend**: [Render API](https://ghci-stjj.onrender.com/docs)

---

## ✨ Key Features

- **High Accuracy**: 97% Accuracy on 50k+ synthetic transactions.
- **Explainable AI**: Uses **SHAP** (SHapley Additive exPlanations) to show *why* a transaction was categorized.
- **Batch Processing**: Upload CSVs or paste multiple transactions for bulk classification.
- **Feedback Loop**: Users can correct predictions, saving data for future retraining.
- **Configurable Taxonomy**: Easily update categories via `config/categories.yaml`.
- **Production Ready**: Dockerized, CI/CD friendly, and scalable.

---

## 🛠️ Tech Stack

- **Core**: Python 3.9+
- **ML**: Scikit-learn (Logistic Regression + TF-IDF), SHAP, MLflow
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit, Pandas
- **DevOps**: Docker, Docker Compose

---

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/DYNOSuprovo/GHCI.git
cd GHCI
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Generate Data & Train Model
```bash
# Generate 50,000 synthetic transactions
python src/data_generator.py

# Train the model (saves to models/model.pkl)
python src/model.py
```

---

## 🏃‍♂️ Running the App

### Option A: Full Stack (API + UI)
**Terminal 1 (Backend):**
```bash
uvicorn app.main:app --reload --port 8000
```
**Terminal 2 (Frontend):**
```bash
streamlit run app/ui.py
```

### Option B: Standalone Streamlit (No API needed)
```bash
streamlit run app/streamlit_app.py
```

### Option C: Docker
```bash
docker-compose up -d
```

---

## 🌐 API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive Swagger UI.

### Endpoints
- `POST /predict`: Classify a single transaction.
- `POST /predict_batch`: Classify a list of transactions.
- `POST /feedback`: Submit user corrections.
- `GET /categories`: Get list of supported categories.

---

## 📂 Project Structure

```
GHCI/
├── app/
│   ├── main.py           # FastAPI Backend
│   ├── ui.py             # Streamlit Frontend (API-based)
│   └── streamlit_app.py  # Standalone Streamlit App
├── config/
│   └── categories.yaml   # Taxonomy Configuration
├── data/                 # Generated datasets & feedback
├── models/               # Trained model artifacts
├── src/
│   ├── data_generator.py # Synthetic data generation
│   ├── model.py          # Model training & evaluation
│   ├── explainability.py # SHAP explanation logic
│   └── preprocessing.py  # Text cleaning
├── Dockerfile            # Container definition
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## ☁️ Deployment

### Streamlit Cloud (Frontend)
1. Fork this repo.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Deploy `app/streamlit_app.py`.

### Render.com (Backend)
1. Create a **Web Service** on Render.
2. Connect your repo.
3. Select **Docker** environment.
4. Deploy!

For detailed instructions, see **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**.

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
