# Deployment Guide - Transaction Categorization System

This guide covers multiple deployment options for your production-ready transaction categorization system.

---

## Option 1: Docker Deployment (Recommended)

### Prerequisites
- Docker installed
- Docker Compose installed

### Steps
```bash
# 1. Navigate to project directory
cd d:\app\GHCI

# 2. Build and run with Docker Compose
docker-compose up -d

# 3. Access the application
# Backend API: http://localhost:8000
# Frontend UI: http://localhost:8501
# API Docs: http://localhost:8000/docs
```

### Verify Deployment
```bash
# Check running containers
docker ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Option 2: Cloud Deployment

### A. **Google Cloud Platform (GCP)**

#### Using Cloud Run (Serverless)
```bash
# 1. Install Google Cloud SDK
# Download from: https://cloud.google.com/sdk/docs/install

# 2. Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# 3. Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/transaction-categorizer

# 4. Deploy to Cloud Run
gcloud run deploy transaction-categorizer \
  --image gcr.io/YOUR_PROJECT_ID/transaction-categorizer \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

**Cost**: Pay-per-use, free tier available

---

### B. **Amazon Web Services (AWS)**

#### Using Elastic Beanstalk
```bash
# 1. Install AWS CLI and EB CLI
pip install awscli awsebcli

# 2. Configure AWS credentials
aws configure

# 3. Initialize EB application
eb init -p docker transaction-categorizer

# 4. Create environment and deploy
eb create production-env
eb deploy
```

#### Using ECS (Elastic Container Service)
- Upload Docker image to ECR (Elastic Container Registry)
- Create ECS cluster and service
- Configure load balancer and auto-scaling

**Cost**: ~$10-50/month depending on usage

---

### C. **Microsoft Azure**

#### Using Azure Container Instances
```bash
# 1. Install Azure CLI
# Download from: https://aka.ms/installazurecliwindows

# 2. Login
az login

# 3. Create resource group
az group create --name transaction-categorizer-rg --location eastus

# 4. Deploy container
az container create \
  --resource-group transaction-categorizer-rg \
  --name transaction-categorizer \
  --image YOUR_DOCKER_IMAGE \
  --dns-name-label transaction-cat \
  --ports 8000 8501
```

**Cost**: ~$15-30/month

---

### D. **Heroku** (Easiest for beginners)

#### Steps
```bash
# 1. Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login
heroku login

# 3. Create app
heroku create transaction-categorizer

# 4. Add Procfile to your project
echo "web: uvicorn app.main:app --host 0.0.0.0 --port $PORT" > Procfile

# 5. Deploy
git push heroku main

# 6. Open app
heroku open
```

**Cost**: Free tier available, paid plans from $7/month

---

### E. **Railway.app** (Modern & Simple)

1. Visit [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Dockerfile and deploys

**Cost**: $5/month per service

---

### F. **DigitalOcean App Platform**

1. Visit [DigitalOcean](https://www.digitalocean.com/products/app-platform)
2. Create account and new app
3. Connect GitHub repository
4. Select Dockerfile deployment
5. Configure resources and deploy

**Cost**: $5-12/month

---

## Option 3: VPS Deployment (Full Control)

### Using a VPS (DigitalOcean, Linode, AWS EC2, etc.)

```bash
# 1. SSH into your server
ssh root@YOUR_SERVER_IP

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 3. Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 4. Clone your repository
git clone YOUR_REPO_URL
cd YOUR_REPO

# 5. Run with Docker Compose
docker-compose up -d

# 6. Setup Nginx reverse proxy (optional but recommended)
sudo apt install nginx
# Configure Nginx to proxy to your app
```

**Cost**: $5-20/month depending on VPS size

---

## Production Configuration

### Environment Variables
Create a `.env` file:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# MLflow Configuration
MLFLOW_TRACKING_URI=./mlruns

# Model Configuration
MODEL_PATH=models/model.pkl
CATEGORIES_PATH=config/categories.yaml

# CORS (if needed)
ALLOWED_ORIGINS=https://yourdomain.com
```

### Security Recommendations
1. **Enable HTTPS**: Use Let's Encrypt for free SSL certificates
2. **Authentication**: Add API key authentication for production
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **CORS**: Configure allowed origins properly
5. **Monitoring**: Setup logging and monitoring (Sentry, DataDog, etc.)

---

## Recommended Deployment Path

**For quick deployment**: Use **Heroku** or **Railway.app**
**For production**: Use **GCP Cloud Run** or **AWS Elastic Beanstalk**
**For full control**: Use **DigitalOcean VPS** with Docker

---

## Post-Deployment Testing

```bash
# Test API endpoint
curl -X POST "https://your-domain.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"description": "STARBUCKS COFFEE", "amount": 5.50}'

# Test batch endpoint
curl -X POST "https://your-domain.com/predict_batch" \
  -H "Content-Type: application/json" \
  -d '{"transactions": [{"description": "UBER", "amount": 15}]}'
```

---

## Monitoring & Maintenance

### MLflow Tracking
- Setup remote MLflow server for experiment tracking
- Or use MLflow hosted services

### Logs
```bash
# Docker logs
docker-compose logs -f

# Or use cloud provider logging
# GCP: Stackdriver
# AWS: CloudWatch
# Azure: Application Insights
```

### Model Updates
```bash
# Retrain model locally
python src/model.py

# Rebuild and redeploy
docker-compose build
docker-compose up -d
```

---

## Cost Comparison

| Platform | Estimated Cost | Ease of Use | Scalability |
|----------|---------------|-------------|-------------|
| Heroku | $7-25/month | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Railway.app | $5-15/month | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| GCP Cloud Run | $5-30/month | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| AWS ECS | $10-50/month | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| DigitalOcean | $5-20/month | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## Need Help?

- Docker issues? Check: https://docs.docker.com/
- Cloud platform docs linked above
- For custom deployment assistance, consult with a DevOps specialist
