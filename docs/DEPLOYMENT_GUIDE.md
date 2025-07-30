# Deployment Guide

This guide covers different deployment options for the Self-Prompting ODQA System.

## Prerequisites

### Required
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Python 3.8+ (for backend)
- Node.js 18+ (for frontend)

### Optional
- Docker and Docker Compose (for containerized deployment)
- Nginx (for production reverse proxy)

## Local Development Setup

### 1. Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd NLP

# Run automated setup
python setup.py

# Configure API key
# Edit backend/.env and add your GEMINI_API_KEY

# Start the system
python run_system.py run
```

### 2. Manual Setup

#### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Unix/Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Start backend
python main.py
```

#### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 3. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Docker Deployment

### 1. Using Docker Compose (Recommended)

```bash
# Create environment file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 2. Using Docker Only

```bash
# Build the image
docker build -t self-prompting-odqa .

# Run the container
docker run -d \
  --name self-prompting-odqa \
  -p 3000:3000 \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_api_key_here \
  -v $(pwd)/data:/app/data \
  self-prompting-odqa
```

## Production Deployment

### 1. With Nginx Reverse Proxy

```bash
# Start with production profile
docker-compose --profile production up -d

# This starts:
# - Main application on internal ports
# - Nginx reverse proxy on port 80
```

### 2. Environment Configuration

Create a production `.env` file:
```bash
GEMINI_API_KEY=your_production_api_key
DATABASE_PATH=/app/data/self_prompting.db
MAX_DEMONSTRATIONS=10
DEFAULT_CLUSTERS=10
TEMPERATURE=0.7
MAX_TOKENS=2048

# Production optimizations
WORKERS=4
LOG_LEVEL=INFO
```

### 3. SSL/HTTPS Setup

For production with SSL, modify `nginx.conf`:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # ... rest of configuration
}

server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## Cloud Deployment

### 1. AWS Deployment

#### Using AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com

docker build -t self-prompting-odqa .
docker tag self-prompting-odqa:latest <account>.dkr.ecr.us-east-1.amazonaws.com/self-prompting-odqa:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/self-prompting-odqa:latest

# Deploy using ECS task definition
```

#### Using AWS EC2
```bash
# On EC2 instance
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Deploy application
git clone <repository-url>
cd NLP
echo "GEMINI_API_KEY=your_api_key" > .env
docker-compose up -d
```

### 2. Google Cloud Platform

#### Using Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/self-prompting-odqa

# Deploy to Cloud Run
gcloud run deploy self-prompting-odqa \
  --image gcr.io/PROJECT_ID/self-prompting-odqa \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_api_key
```

### 3. Azure Container Instances

```bash
# Create resource group
az group create --name self-prompting-rg --location eastus

# Deploy container
az container create \
  --resource-group self-prompting-rg \
  --name self-prompting-odqa \
  --image your-registry/self-prompting-odqa:latest \
  --dns-name-label self-prompting-odqa \
  --ports 80 3000 8000 \
  --environment-variables GEMINI_API_KEY=your_api_key
```

## Monitoring and Maintenance

### 1. Health Checks

The system provides health check endpoints:
```bash
# Backend health
curl http://localhost:8000/health

# System status
curl http://localhost:8000/status
```

### 2. Logging

#### Docker Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f self-prompting-odqa
```

#### Application Logs
Logs are written to stdout/stderr and can be collected by your logging system.

### 3. Backup and Recovery

#### Database Backup
```bash
# Backup SQLite database
cp data/self_prompting.db data/backup_$(date +%Y%m%d_%H%M%S).db

# Or using Docker
docker-compose exec self-prompting-odqa cp /app/data/self_prompting.db /app/data/backup.db
```

#### Full System Backup
```bash
# Backup entire data directory
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz data/
```

## Performance Tuning

### 1. System Resources

Recommended minimum resources:
- **CPU**: 2 cores
- **RAM**: 4GB (8GB recommended for dataset generation)
- **Storage**: 10GB (for dataset and embeddings)

### 2. Configuration Tuning

```bash
# Increase worker processes for production
WORKERS=4

# Adjust clustering parameters
DEFAULT_CLUSTERS=15
MAX_DEMONSTRATIONS=12

# Optimize API calls
TEMPERATURE=0.5
MAX_TOKENS=1024
```

### 3. Caching

For high-traffic deployments, consider adding Redis caching:
```yaml
# Add to docker-compose.yml
redis:
  image: redis:alpine
  ports:
    - "6379:6379"
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   ```bash
   # Check if API key is set
   echo $GEMINI_API_KEY
   
   # Test API access
   python -c "from backend.gemini_client import GeminiClient; print(GeminiClient().generate_text('Hello'))"
   ```

2. **Database Issues**
   ```bash
   # Check database file permissions
   ls -la data/
   
   # Reset database
   rm data/self_prompting.db
   # Restart system to recreate
   ```

3. **Memory Issues**
   ```bash
   # Monitor memory usage
   docker stats
   
   # Increase Docker memory limit
   # Docker Desktop: Settings > Resources > Memory
   ```

4. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :3000
   
   # Use different ports
   docker-compose up -d -p 8001:8000 -p 3001:3000
   ```

### Getting Help

1. Check the logs for error messages
2. Verify all environment variables are set
3. Ensure API key has sufficient quota
4. Test individual components using the test suite
5. Check system status via the web interface

For additional support, refer to the system architecture documentation and the original research paper.
