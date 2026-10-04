# FaithMetrics - Deployment Guide

## 🚀 Deployment Options

This guide covers multiple deployment strategies for the FaithMetrics platform, from local development to cloud production.

---

## 1️⃣ Local Development

### Prerequisites
- Python 3.9+
- pip
- Git (optional)

### Setup Steps

```bash
# 1. Navigate to project directory
cd faithmetrics

# 2. Create virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate data (if needed)
python generate_church_data.py

# 5. Run application
streamlit run faithmetrics_app.py
```

### Access
- Local URL: `http://localhost:8501`
- Network URL: `http://<your-ip>:8501`

---

## 2️⃣ Streamlit Community Cloud (FREE)

### Why Streamlit Cloud?
- ✅ Free hosting for public apps
- ✅ Automatic deployments from GitHub
- ✅ Built-in HTTPS and custom domains
- ✅ No DevOps required

### Deployment Steps

1. **Prepare Repository**
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit - FaithMetrics platform"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/faithmetrics.git
git push -u origin main
```

2. **Deploy to Streamlit Cloud**
- Visit: https://share.streamlit.io
- Sign in with GitHub
- Click "New app"
- Select your repository
- Main file: `faithmetrics_app.py`
- Click "Deploy"

3. **Configuration**
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#f8f9fa"
secondaryBackgroundColor = "#ffffff"
textColor = "#2c3e50"
font = "sans serif"

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false
```

### Custom Domain (Optional)
- Go to app settings
- Add custom domain: `faithmetrics.yourchurch.org`
- Update DNS CNAME record

---

## 3️⃣ Docker Deployment

### Why Docker?
- ✅ Consistent environment
- ✅ Easy scaling
- ✅ Works anywhere (AWS, Azure, GCP, local)

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Generate data on first run
RUN python generate_church_data.py

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "faithmetrics_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  faithmetrics:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
    restart: unless-stopped
```

### Build and Run
```bash
# Build image
docker build -t faithmetrics .

# Run container
docker run -p 8501:8501 faithmetrics

# Or use docker-compose
docker-compose up -d
```

---

## 4️⃣ AWS Deployment (Production)

### Option A: AWS Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB Application**
```bash
eb init -p docker faithmetrics-app
```

3. **Create Environment**
```bash
eb create faithmetrics-prod
```

4. **Deploy**
```bash
eb deploy
```

### Option B: AWS ECS (Container Service)

1. **Push to ECR**
```bash
# Authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag faithmetrics:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/faithmetrics:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/faithmetrics:latest
```

2. **Create ECS Task Definition**
```json
{
  "family": "faithmetrics-task",
  "containerDefinitions": [
    {
      "name": "faithmetrics",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/faithmetrics:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "memory": 512,
      "cpu": 256
    }
  ]
}
```

3. **Create ECS Service with Load Balancer**

### Option C: AWS EC2 (Manual)

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@<instance-ip>

# Install Docker
sudo yum update -y
sudo yum install docker -y
sudo service docker start

# Clone repository
git clone https://github.com/yourusername/faithmetrics.git
cd faithmetrics

# Run with Docker
sudo docker build -t faithmetrics .
sudo docker run -d -p 80:8501 faithmetrics
```

---

## 5️⃣ Google Cloud Platform

### Cloud Run (Serverless)

1. **Build and Push to GCR**
```bash
# Authenticate
gcloud auth configure-docker

# Build
gcloud builds submit --tag gcr.io/PROJECT-ID/faithmetrics

# Deploy
gcloud run deploy faithmetrics \
  --image gcr.io/PROJECT-ID/faithmetrics \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

2. **Custom Domain**
```bash
gcloud run domain-mappings create \
  --service faithmetrics \
  --domain faithmetrics.yourchurch.org
```

---

## 6️⃣ Microsoft Azure

### Azure App Service

1. **Create App Service**
```bash
az webapp up --name faithmetrics --runtime "PYTHON:3.11"
```

2. **Deploy from GitHub**
- Go to Azure Portal
- Select your App Service
- Deployment Center → GitHub
- Select repository and branch

---

## 🔒 Security Best Practices

### Environment Variables
Never hardcode sensitive data. Use environment variables:

```python
# In your app
import os

# Example: Database connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PASSWORD = os.getenv('DB_PASSWORD')
```

### Secrets Management

**AWS Secrets Manager**
```bash
aws secretsmanager create-secret \
  --name faithmetrics/db-password \
  --secret-string "your-secure-password"
```

**Docker Secrets**
```yaml
# docker-compose.yml
secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### HTTPS/SSL
Always use HTTPS in production:
- Streamlit Cloud: Automatic
- AWS: Use Certificate Manager + ALB
- Custom: Let's Encrypt + Nginx

---

## 📊 Monitoring & Logging

### Streamlit Cloud
- Built-in analytics dashboard
- Real-time logs in web interface

### AWS CloudWatch
```python
import watchtower
import logging

logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

### Google Cloud Logging
```bash
gcloud run services update faithmetrics \
  --set-env-vars GOOGLE_CLOUD_PROJECT=PROJECT-ID
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          pytest tests/
      
      - name: Deploy
        run: |
          # Streamlit Cloud auto-deploys from main branch
          echo "Deployment triggered"
```

---

## 📈 Performance Optimization

### Caching Strategies
```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    # Your data loading logic
    pass

@st.cache_resource
def init_ml_model():
    # Load ML model once
    pass
```

### Database Connection Pooling
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'postgresql://user:pass@host/db',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError"
```bash
# Solution: Ensure all dependencies installed
pip install -r requirements.txt --upgrade
```

**Issue**: "Port already in use"
```bash
# Solution: Use different port
streamlit run faithmetrics_app.py --server.port=8502
```

**Issue**: "Data files not found"
```bash
# Solution: Generate data
python generate_church_data.py
```

### Debugging
```bash
# Run with debug logging
streamlit run faithmetrics_app.py --logger.level=debug
```

---

## 📱 Mobile Optimization

The app is responsive, but for native mobile:

### Progressive Web App (PWA)

Create `manifest.json`:
```json
{
  "name": "FaithMetrics",
  "short_name": "FaithMetrics",
  "description": "Church Analytics Platform",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#667eea",
  "theme_color": "#667eea",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    }
  ]
}
```

---

## 💾 Database Migration (Optional)

### From CSV to PostgreSQL

```python
import pandas as pd
from sqlalchemy import create_engine

# Create engine
engine = create_engine('postgresql://user:pass@host/faithmetrics')

# Migrate data
members_df.to_sql('members', engine, if_exists='replace', index=False)
attendance_df.to_sql('attendance', engine, if_exists='replace', index=False)
donations_df.to_sql('donations', engine, if_exists='replace', index=False)
```

Update app to use PostgreSQL:
```python
@st.cache_data
def load_data():
    engine = create_engine(os.getenv('DATABASE_URL'))
    members = pd.read_sql('SELECT * FROM members', engine)
    # ... load other tables
    return members, attendance, donations, events, sermons
```

---

## ✅ Pre-Deployment Checklist

- [ ] All dependencies in requirements.txt
- [ ] Environment variables configured
- [ ] Data generation tested
- [ ] HTTPS enabled
- [ ] Monitoring configured
- [ ] Backup strategy in place
- [ ] Error handling tested
- [ ] Performance optimized
- [ ] Security audit completed
- [ ] Documentation updated

---

## 🎯 Recommended Deployment

**For Demonstration:**
1. **Streamlit Community Cloud** - Quick, free, professional URL
2. **GitHub Repository** - Showcase code quality and documentation
3. **Demo Video** - Record walkthrough of key features

**For Production Use:**
1. **AWS ECS/Fargate** - Scalable, enterprise-ready
2. **PostgreSQL RDS** - Managed database
3. **CloudFront CDN** - Global performance
4. **Route 53** - Custom domain management

---

## 📞 Support

For deployment issues:
1. Check Streamlit documentation: https://docs.streamlit.io
2. Review platform-specific guides (AWS/GCP/Azure)
3. Contact: P (DigiTech Edge Solutions)

---

**Happy Deploying! 🚀**

*FaithMetrics - Empowering churches through data-driven insights*
