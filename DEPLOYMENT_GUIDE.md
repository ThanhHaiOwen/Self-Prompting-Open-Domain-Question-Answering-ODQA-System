# 🚀 Deployment Guide - Self-Prompting ODQA System

This guide provides comprehensive instructions for deploying the Self-Prompting ODQA System in various environments.

## 📋 **Prerequisites**

### **System Requirements**
- **Python**: 3.8 or higher
- **Node.js**: 16 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space
- **Network**: Internet connection for Gemini API

### **API Requirements**
- **Google Gemini API Key**: Required for LLM processing
- Get your API key from: https://makersuite.google.com/app/apikey

## 🏠 **Local Development Setup**

### **1. Clone Repository**
```bash
git clone https://github.com/yourusername/self-prompting-odqa.git
cd self-prompting-odqa
```

### **2. Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

### **3. Frontend Setup**
```bash
cd ../frontend

# Install dependencies
npm install

# Optional: Update dependencies
npm update
```

### **4. Start Services**

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### **5. Verify Installation**
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Status: http://localhost:8000/status

## 🐳 **Docker Deployment**

### **Using Docker Compose (Recommended)**
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop services
docker-compose down
```

### **Manual Docker Build**
```bash
# Build backend
docker build -t odqa-backend ./backend

# Build frontend
docker build -t odqa-frontend ./frontend

# Run backend
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key odqa-backend

# Run frontend
docker run -p 3000:3000 odqa-frontend
```

## ☁️ **Cloud Deployment**

### **Heroku Deployment**

1. **Install Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
sudo snap install --classic heroku
```

2. **Deploy Backend**
```bash
cd backend
heroku create your-odqa-backend
heroku config:set GEMINI_API_KEY=your_api_key
git subtree push --prefix backend heroku main
```

3. **Deploy Frontend**
```bash
cd frontend
heroku create your-odqa-frontend
heroku buildpacks:set mars/create-react-app
git subtree push --prefix frontend heroku main
```

### **AWS EC2 Deployment**

1. **Launch EC2 Instance**
- AMI: Ubuntu 20.04 LTS
- Instance Type: t3.medium (minimum)
- Security Groups: Allow ports 22, 80, 443, 3000, 8000

2. **Setup Server**
```bash
# Connect to instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip nodejs npm nginx -y

# Clone repository
git clone https://github.com/yourusername/self-prompting-odqa.git
cd self-prompting-odqa
```

3. **Configure Services**
```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key" > .env

# Frontend setup
cd ../frontend
npm install
npm run build
```

4. **Setup Nginx**
```bash
sudo cp nginx.conf /etc/nginx/sites-available/odqa
sudo ln -s /etc/nginx/sites-available/odqa /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **Google Cloud Platform**

1. **Setup GCP Project**
```bash
gcloud init
gcloud app create --region=us-central
```

2. **Deploy Backend**
```bash
cd backend
gcloud app deploy app.yaml
```

3. **Deploy Frontend**
```bash
cd frontend
npm run build
gsutil -m cp -r build/* gs://your-bucket-name
```

## 🔧 **Production Configuration**

### **Environment Variables**
```bash
# Backend (.env)
GEMINI_API_KEY=your_production_api_key
DATABASE_URL=sqlite:///data/qa_pairs.db
LOG_LEVEL=INFO
CORS_ORIGINS=https://your-frontend-domain.com

# Frontend (.env.production)
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_ENVIRONMENT=production
```

### **Database Optimization**
```bash
# Backup database
cp backend/data/qa_pairs.db backend/data/qa_pairs_backup.db

# Optimize database
sqlite3 backend/data/qa_pairs.db "VACUUM; ANALYZE;"
```

### **Performance Tuning**
```python
# backend/config.py
WORKERS = 4  # Number of worker processes
MAX_CONNECTIONS = 100
TIMEOUT = 30
CACHE_TTL = 3600  # 1 hour cache
```

## 📊 **Monitoring & Logging**

### **Health Checks**
```bash
# Backend health
curl http://localhost:8000/health

# System status
curl http://localhost:8000/status

# Database check
curl http://localhost:8000/dataset/stats
```

### **Log Monitoring**
```bash
# Backend logs
tail -f backend/logs/app.log

# System logs
journalctl -u odqa-backend -f
```

## 🔒 **Security Considerations**

### **API Security**
- Store API keys in environment variables
- Use HTTPS in production
- Implement rate limiting
- Add CORS restrictions

### **Database Security**
- Regular backups
- Access control
- Encryption at rest

### **Network Security**
- Firewall configuration
- VPN access for admin
- SSL/TLS certificates

## 🚨 **Troubleshooting**

### **Common Issues**

1. **API Key Errors**
```bash
# Check environment variable
echo $GEMINI_API_KEY

# Verify API key validity
curl -H "Authorization: Bearer $GEMINI_API_KEY" https://generativelanguage.googleapis.com/v1/models
```

2. **Database Issues**
```bash
# Check database file
ls -la backend/data/qa_pairs.db

# Verify database content
sqlite3 backend/data/qa_pairs.db ".tables"
```

3. **Port Conflicts**
```bash
# Check port usage
lsof -i :8000
lsof -i :3000

# Kill processes if needed
kill -9 $(lsof -t -i:8000)
```

4. **Memory Issues**
```bash
# Check memory usage
free -h
top -p $(pgrep -f "python main.py")
```

## 📈 **Scaling Considerations**

### **Horizontal Scaling**
- Load balancer configuration
- Multiple backend instances
- Database replication
- CDN for frontend assets

### **Vertical Scaling**
- Increase server resources
- Optimize database queries
- Implement caching layers
- Use async processing

## 🔄 **Backup & Recovery**

### **Database Backup**
```bash
# Create backup
sqlite3 backend/data/qa_pairs.db ".backup backup_$(date +%Y%m%d).db"

# Restore backup
cp backup_20241201.db backend/data/qa_pairs.db
```

### **Full System Backup**
```bash
# Create system backup
tar -czf odqa_backup_$(date +%Y%m%d).tar.gz \
  --exclude=node_modules \
  --exclude=venv \
  --exclude=__pycache__ \
  .
```

---

## 📞 **Support**

For deployment issues:
1. Check the troubleshooting section
2. Review logs for error messages
3. Verify all prerequisites are met
4. Contact support with specific error details

**Happy Deploying! 🚀**
