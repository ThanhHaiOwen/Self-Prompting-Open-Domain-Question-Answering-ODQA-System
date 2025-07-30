#!/bin/bash

# 🧠 Self-Prompting ODQA System - Quick Start Script
# This script helps you run the complete system with one command

echo "🧠 Self-Prompting ODQA System"
echo "============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "backend/main.py" ] || [ ! -f "frontend/package.json" ]; then
    print_error "Please run this script from the project root directory."
    exit 1
fi

print_info "Starting Self-Prompting ODQA System setup..."
echo ""

# Backend Setup
print_info "Setting up backend..."

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
if [ ! -f "venv/pyvenv.cfg" ] || [ ! -f "venv/lib/python*/site-packages/fastapi" ]; then
    print_info "Installing Python dependencies..."
    pip install -r requirements.txt
    print_status "Python dependencies installed"
else
    print_status "Python dependencies already installed"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    print_warning "No .env file found. Creating template..."
    echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
    print_warning "Please edit backend/.env and add your Gemini API key"
    print_info "Get your API key from: https://makersuite.google.com/app/apikey"
    echo ""
fi

# Check if database exists
if [ ! -f "data/qa_pairs.db" ]; then
    print_warning "Database not found. The system will create it automatically."
fi

cd ..

# Frontend Setup
print_info "Setting up frontend..."

cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_info "Installing Node.js dependencies..."
    npm install
    print_status "Node.js dependencies installed"
else
    print_status "Node.js dependencies already installed"
fi

cd ..

print_status "Setup completed!"
echo ""

# Function to start backend
start_backend() {
    print_info "Starting backend server..."
    cd backend
    source venv/bin/activate
    python main.py &
    BACKEND_PID=$!
    cd ..
    
    # Wait for backend to start
    print_info "Waiting for backend to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_status "Backend server started successfully on http://localhost:8000"
            return 0
        fi
        sleep 1
    done
    
    print_error "Backend failed to start within 30 seconds"
    return 1
}

# Function to start frontend
start_frontend() {
    print_info "Starting frontend server..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    
    # Wait for frontend to start
    print_info "Waiting for frontend to start..."
    for i in {1..60}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            print_status "Frontend server started successfully on http://localhost:3000"
            return 0
        fi
        sleep 1
    done
    
    print_error "Frontend failed to start within 60 seconds"
    return 1
}

# Function to cleanup on exit
cleanup() {
    echo ""
    print_info "Shutting down servers..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        print_status "Backend server stopped"
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_status "Frontend server stopped"
    fi
    
    # Kill any remaining processes
    pkill -f "python main.py" 2>/dev/null
    pkill -f "npm start" 2>/dev/null
    
    print_status "System shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Check command line arguments
case "${1:-start}" in
    "start")
        print_info "Starting complete system..."
        echo ""
        
        # Start backend
        if start_backend; then
            # Start frontend
            if start_frontend; then
                echo ""
                print_status "🎉 System started successfully!"
                echo ""
                echo "📊 Access Points:"
                echo "   Frontend: http://localhost:3000"
                echo "   Backend:  http://localhost:8000"
                echo "   API Docs: http://localhost:8000/docs"
                echo ""
                echo "🧪 Test the system:"
                echo "   curl -X POST http://localhost:8000/ask \\"
                echo "     -H \"Content-Type: application/json\" \\"
                echo "     -d '{\"question\": \"What was Google originally called?\"}'"
                echo ""
                print_info "Press Ctrl+C to stop the system"
                
                # Keep script running
                while true; do
                    sleep 1
                done
            else
                cleanup
                exit 1
            fi
        else
            cleanup
            exit 1
        fi
        ;;
    
    "backend")
        print_info "Starting backend only..."
        start_backend
        if [ $? -eq 0 ]; then
            print_info "Press Ctrl+C to stop the backend"
            wait $BACKEND_PID
        fi
        ;;
    
    "frontend")
        print_info "Starting frontend only..."
        start_frontend
        if [ $? -eq 0 ]; then
            print_info "Press Ctrl+C to stop the frontend"
            wait $FRONTEND_PID
        fi
        ;;
    
    "test")
        print_info "Running system tests..."
        
        # Test backend
        cd backend
        source venv/bin/activate
        python -c "
import requests
import sys

try:
    # Test if backend is running
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.status_code == 200:
        print('✅ Backend is running')
    else:
        print('❌ Backend health check failed')
        sys.exit(1)
        
    # Test API
    response = requests.post('http://localhost:8000/ask', 
                           json={'question': 'What was Google originally called?'},
                           timeout=10)
    if response.status_code == 200:
        data = response.json()
        if 'answer' in data:
            print(f'✅ API test successful: {data[\"answer\"]}')
        else:
            print('❌ API response missing answer')
            sys.exit(1)
    else:
        print('❌ API test failed')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ Test failed: {e}')
    sys.exit(1)
"
        cd ..
        ;;
    
    "help"|"-h"|"--help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  start     Start both backend and frontend (default)"
        echo "  backend   Start backend only"
        echo "  frontend  Start frontend only"
        echo "  test      Test if system is running"
        echo "  help      Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0                # Start complete system"
        echo "  $0 start          # Start complete system"
        echo "  $0 backend        # Start backend only"
        echo "  $0 frontend       # Start frontend only"
        echo "  $0 test           # Test system"
        ;;
    
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
