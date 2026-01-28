#!/bin/bash

# Voice Assistant Quick Start Script
# This script will help you set up and run the voice assistant

echo "Voice Assistant Setup Script"
echo "================================"
echo ""

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Found: $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Warning: Please edit .env and add your Google Gemini API key"
    echo "   Get your key from: https://aistudio.google.com/apikey"
    echo ""
    read -p "Press Enter to continue after adding your API key..."
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p static/css static/js templates logs
echo "Directories created"
echo ""

# Run the application
echo "Starting the voice assistant..."
echo "   Access it at: http://localhost:8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
python3 -m src.app