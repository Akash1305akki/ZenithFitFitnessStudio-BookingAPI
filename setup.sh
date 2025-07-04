#!/bin/bash

# Setup script to initialize and run the app

echo "Creating virtual environment..."
python -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running FastAPI server..."
uvicorn main:app --reload
