#!/bin/bash

echo "=========================================="
echo "  FaithMetrics - Church Analytics Platform"
echo "  Quick Start Script"
echo "=========================================="
echo ""

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check if data exists
if [ ! -f "data_members.csv" ]; then
    echo "🔄 Generating synthetic church data..."
    python generate_church_data.py
    
    if [ $? -eq 0 ]; then
        echo "✅ Data generated successfully"
    else
        echo "❌ Failed to generate data"
        exit 1
    fi
else
    echo "✅ Data files already exist"
fi

echo ""
echo "=========================================="
echo "  🚀 Starting FaithMetrics..."
echo "=========================================="
echo ""
echo "📊 The application will open in your browser"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Run Streamlit
streamlit run faithmetrics_app.py
