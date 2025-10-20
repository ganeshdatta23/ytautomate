#!/bin/bash
# Quick run script for Linux/Mac

echo "========================================"
echo "YouTube Automation - Quick Run"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies if needed
if [ ! -d "venv/lib/python*/site-packages/edge_tts" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run based on argument
case "$1" in
    test)
        echo "Running system test..."
        python test_system.py
        ;;
    setup)
        echo "Running setup..."
        python setup.py
        ;;
    batch)
        echo "Generating batch videos..."
        python main.py --mode batch --count ${2:-5} --no-upload
        ;;
    *)
        echo "Generating single video..."
        python main.py --mode single --no-upload
        ;;
esac

echo ""
echo "========================================"
echo "Done!"
echo "========================================"
