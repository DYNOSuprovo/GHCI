FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Generate data and train model during build
ENV PYTHONPATH=/app
RUN python src/data_generator.py
RUN python src/model.py

# Create a script to run both services
RUN echo '#!/bin/bash\n\
    uvicorn app.main:app --host 0.0.0.0 --port 8000 & \n\
    streamlit run app/ui.py --server.port 8501 --server.address 0.0.0.0\n\
    ' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
