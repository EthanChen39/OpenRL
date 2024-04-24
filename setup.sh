#!/bin/bash

# Step 1: Create a Python virtual environment named ".venv"
echo "Creating a virtual environment..."
python -m venv .venv

# Step 2: Activate the virtual environment
echo "Activating the virtual environment..."
source .venv/bin/activate

# Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 3: Install pre-commit
echo "Installing pre-commit..."
pip install pre-commit

# Step 4: Install hooks in pre-commit
echo "Installing hooks in pre-commit..."
pre-commit install

echo "Setup completed successfully."
