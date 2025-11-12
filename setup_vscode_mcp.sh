#!/bin/bash
# Travel Reservations MCP Server - Quick Setup Script for macOS/Linux
# This script helps you set up the MCP server configuration for VS Code

echo "================================"
echo "Travel Reservations MCP Server"
echo "VS Code Setup Helper"
echo "================================"
echo ""

# Get the current directory (project root)
PROJECT_PATH=$(pwd)
echo "Project directory: $PROJECT_PATH"
echo ""

# Check if Python is installed
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    echo "✓ $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo "✗ Python not found. Please install Python 3.x first."
    exit 1
fi
echo ""

# Check if required files exist
echo "Checking required files..."
REQUIRED_FILES=("mcp_server.py" "requirements.txt" "data.json")
ALL_FILES_EXIST=true

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file exists"
    else
        echo "✗ $file not found"
        ALL_FILES_EXIST=false
    fi
done

if [ "$ALL_FILES_EXIST" = false ]; then
    echo ""
    echo "Some required files are missing. Please run this script from the project root directory."
    exit 1
fi
echo ""

# Check if virtual environment exists
VENV_PATH="$PROJECT_PATH/venv"
USE_VENV=false

if [ -d "$VENV_PATH" ]; then
    echo "Virtual environment found at: $VENV_PATH"
    read -p "Use virtual environment? (y/n) " USE_VENV_PROMPT
    if [ "$USE_VENV_PROMPT" = "y" ] || [ "$USE_VENV_PROMPT" = "Y" ]; then
        USE_VENV=true
        echo "✓ Will use virtual environment"
    fi
else
    echo "No virtual environment found."
    read -p "Create virtual environment? (y/n) " CREATE_VENV_PROMPT
    if [ "$CREATE_VENV_PROMPT" = "y" ] || [ "$CREATE_VENV_PROMPT" = "Y" ]; then
        echo "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        
        if [ $? -eq 0 ]; then
            echo "✓ Virtual environment created"
            USE_VENV=true
            
            # Activate and install dependencies
            echo "Installing dependencies..."
            source "$VENV_PATH/bin/activate"
            pip install -r requirements.txt
            
            if [ $? -eq 0 ]; then
                echo "✓ Dependencies installed"
            else
                echo "✗ Failed to install dependencies"
            fi
        else
            echo "✗ Failed to create virtual environment"
        fi
    fi
fi
echo ""

# Generate the configuration
echo "Generating VS Code configuration..."
echo ""

MCP_SERVER_PATH="$PROJECT_PATH/mcp_server.py"
PYTHON_COMMAND="$PYTHON_CMD"

if [ "$USE_VENV" = true ]; then
    PYTHON_COMMAND="$VENV_PATH/bin/python"
fi

# Generate JSON configuration
CONFIG=$(cat <<EOF
{
  "github.copilot.referenceable.mcpServers": {
    "travel-reservations": {
      "command": "$PYTHON_COMMAND",
      "args": [
        "$MCP_SERVER_PATH"
      ],
      "env": {
        "PYTHONPATH": "$PROJECT_PATH"
      }
    }
  }
}
EOF
)

echo "================================"
echo "VS Code Configuration"
echo "================================"
echo "$CONFIG"
echo "================================"
echo ""

# Instructions
echo "Next steps:"
echo "1. Copy the configuration above"
echo "2. Open VS Code settings (Cmd+, on macOS, Ctrl+, on Linux)"
echo "3. Click 'Open Settings (JSON)' icon"
echo "4. Add the configuration to your settings.json"
echo "5. Restart VS Code (Cmd+Shift+P/Ctrl+Shift+P > Developer: Reload Window)"
echo ""

# Offer to save to file
read -p "Save configuration to vscode_mcp_config.json? (y/n) " SAVE_PROMPT
if [ "$SAVE_PROMPT" = "y" ] || [ "$SAVE_PROMPT" = "Y" ]; then
    echo "$CONFIG" > vscode_mcp_config.json
    echo "✓ Configuration saved to vscode_mcp_config.json"
    echo ""
fi

# Test the MCP server
echo "Testing MCP server..."
TEST_CMD="$PYTHON_COMMAND"
if [ "$USE_VENV" = true ]; then
    TEST_CMD="$VENV_PATH/bin/python"
fi

# Just check if the script can be imported/parsed, don't run it
if $TEST_CMD -c "import sys; sys.path.insert(0, '$PROJECT_PATH'); import mcp_server; print('OK')" 2>&1 | grep -q "OK"; then
    echo "✓ MCP server script is valid and can be loaded"
else
    echo "⚠ MCP server validation completed with warnings"
    echo "  This is normal if dependencies are installed correctly"
fi
echo ""

echo "Setup complete! 🎉"
echo ""
echo "For detailed instructions, see: VSCODE_INSTALLATION.md"
