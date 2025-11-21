#!/bin/bash

# Script to run infrastructure tests for InfraStack
# This script handles virtual environment setup and runs pytest

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Infrastructure Tests ===${NC}\n"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv .venv
    echo -e "${GREEN}Virtual environment created.${NC}\n"
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import aws_cdk" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install --quiet -r requirements.txt
    pip install --quiet -r requirements-dev.txt
    echo -e "${GREEN}Dependencies installed.${NC}\n"
fi

# Run tests
echo -e "${BLUE}Running tests...${NC}\n"
python -m pytest tests/unit/test_infra_stack.py -v "$@"

# Check test result
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ All tests passed!${NC}"
else
    echo -e "\n${YELLOW}✗ Some tests failed.${NC}"
    exit 1
fi
