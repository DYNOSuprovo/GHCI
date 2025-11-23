# FREE Deployment Options

## 🎯 Best FREE Options (Ranked)

### 1. **Render.com** ⭐ RECOMMENDED
**100% FREE** with no credit card required!

#### Features
- Free tier: 750 hours/month
- Auto-deploy from GitHub
- Free SSL certificates
- No credit card needed

#### Deploy Steps
```bash
# 1. Push code to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main

# 2. Visit render.com and sign up
# 3. Click "New +" → "Web Service"
# 4. Connect your GitHub repo
# 5. Configure:
#    - Name: transaction-categorizer
#    - Environment: Docker
#    - Plan: Free
# 6. Click "Create Web Service"
```

**URL**: Your app will be at `https://transaction-categorizer.onrender.com`

---

### 2. **Railway.app** ⭐ EXCELLENT
**$5 free credit/month** (renews monthly!)

#### Features
- $5 credit = ~500 hours of runtime
- Easiest deployment
- Auto-deploys from GitHub
- Great for hobby projects

#### Deploy Steps
```bash
# 1. Visit railway.app
# 2. Sign up with GitHub (free)
# 3. Click "New Project" → "Deploy from GitHub repo"
# 4. Select your repository
# 5. Railway auto-detects Dockerfile
# 6. Click "Deploy"
```

**URL**: Railway provides a custom URL like `https://transaction-categorizer.up.railway.app`

---

### 3. **Fly.io**
**FREE tier**: 3 shared CPUs, 256MB RAM

#### Features
- Generous free tier
- Global CDN
- Free SSL

#### Deploy Steps
```bash
# 1. Install Fly CLI
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# 2. Login
fly auth login

# 3. Launch app
fly launch

# 4. Deploy
fly deploy
```

---

### 4. **Hugging Face Spaces** (For ML Apps)
**100% FREE** for public apps!

#### Features
- Perfect for ML/AI apps
- Great community
- Free GPU available
- Public only (code visible)

#### Deploy Steps
```bash
# 1. Create account at huggingface.co
# 2. Create new Space
# 3. Choose "Gradio" or "Streamlit"
# 4. Upload your code
# 5. Add requirements.txt
```

**Note**: You'll need to adapt the Streamlit UI slightly

---

### 5. **Streamlit Community Cloud**
**100% FREE** for Streamlit apps!

#### Features
- Perfect for data apps
- 1GB resources
- Auto-deploys from GitHub
- Built specifically for Streamlit

#### Deploy Steps
```bash
# 1. Push to GitHub (public repo)
git push origin main

# 2. Visit share.streamlit.io
# 3. Sign in with GitHub
# 4. Click "New app"
# 5. Select your repo and main file: app/ui.py
# 6. Click "Deploy"
```

**Limitation**: Only deploys the Streamlit UI, not the FastAPI backend
**Workaround**: Run FastAPI as a separate free service on Render.com

---

## 🏆 MY RECOMMENDATION

### Best Setup: **Render.com (Backend) + Streamlit Cloud (Frontend)**

#### Step 1: Deploy Backend on Render.com
```bash
# Create a new file: render.yaml
services:
  - type: web
    name: transaction-api
    env: docker
    dockerfilePath: ./Dockerfile
    dockerContext: .
    plan: free
```

Then:
1. Visit render.com
2. New → Web Service
3. Connect GitHub repo
4. Select "Docker"
5. Deploy (FREE!)

You'll get URL: `https://transaction-api.onrender.com`

#### Step 2: Deploy Frontend on Streamlit Cloud
1. Update `app/ui.py` to use your Render API URL:
```python
API_URL = "https://transaction-api.onrender.com"
```

2. Visit share.streamlit.io
3. Deploy from GitHub
4. Select `app/ui.py` as main file

You'll get URL: `https://your-app.streamlit.app`

**Total Cost**: $0.00/month! 🎉

---

## Quick Comparison

| Platform | Free Tier | Ease | Best For |
|----------|-----------|------|----------|
| **Render.com** | 750 hrs/month | ⭐⭐⭐⭐⭐ | Full apps |
| **Railway.app** | $5 credit/month | ⭐⭐⭐⭐⭐ | Any app |
| **Fly.io** | 3 CPUs, 256MB | ⭐⭐⭐⭐ | Lightweight apps |
| **Streamlit Cloud** | 1GB, unlimited | ⭐⭐⭐⭐⭐ | Streamlit only |
| **Hugging Face** | Unlimited | ⭐⭐⭐⭐ | ML/AI demos |

---

## Prepare Your Project for Render.com

### Create `render.yaml`
```yaml
services:
  - type: web
    name: transaction-categorizer-api
    env: docker
    plan: free
    healthCheckPath: /
```

### Update Dockerfile (if needed)
Your existing Dockerfile should work! Just make sure:
```dockerfile
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Post-Deployment

### Test Your Deployed API
```bash
# Replace with your Render URL
curl https://your-app.onrender.com/categories
```

### Monitor Usage
- **Render**: Dashboard shows uptime (750 hrs free/month)
- **Railway**: Dashboard shows credit usage ($5/month)
- **Streamlit**: Unlimited for public apps

---

## Limitations to Know

### Render.com Free Tier
- ⚠️ Sleeps after 15 min of inactivity
- ⚠️ Takes ~30s to wake up on first request
- ✅ Perfect for demos and testing

### Railway Free Tier
- ⚠️ $5 credit runs out if heavily used
- ✅ Can add payment method for overages

### Solutions
1. **Prevent sleep**: Use a service like [UptimeRobot](https://uptimerobot.com) (free) to ping your app every 5 minutes
2. **Upgrade if needed**: Render Pro is $7/month for always-on

---

## Ready to Deploy?

### Quickest Path (5 minutes):
1. **Push to GitHub** (if not already)
2. **Visit render.com**
3. **Click "New Web Service"**
4. **Connect GitHub repo**
5. **Select Docker**
6. **Click Deploy**

Done! Your app will be live at `https://your-app.onrender.com` 🚀
