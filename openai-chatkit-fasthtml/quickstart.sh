#!/bin/bash
# Quick start script for ChatKit FastHTML

set -e

echo "🚀 ChatKit FastHTML - Quick Start"
echo "=================================="
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create .env file
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  Please update .env with your credentials:"
    echo "   - OPENAI_API_KEY"
    echo "   - CHATKIT_WORKFLOW_ID"
    echo ""
fi

# Show next steps
echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your OpenAI and ChatKit credentials"
echo "2. Run the development server:"
echo "   make dev"
echo ""
echo "Other commands:"
echo "   make test     - Run tests"
echo "   make lint     - Lint code"
echo "   make format   - Format code"
echo ""
echo "Documentation:"
echo "   README.md              - Getting started"
echo "   ARCHITECTURE.md        - Architecture overview"
echo "   MIGRATION_GUIDE.md     - Migration from Next.js"
echo "   CODE_COMPARISON.md     - Code comparison"
echo "   DEPLOYMENT.md          - Deployment guides"
echo ""
