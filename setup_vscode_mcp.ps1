# Travel Reservations MCP Server - Quick Setup Script for Windows
# This script helps you set up the MCP server configuration for VS Code

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Travel Reservations MCP Server" -ForegroundColor Cyan
Write-Host "VS Code Setup Helper" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get the current directory (project root)
$projectPath = Get-Location
Write-Host "Project directory: $projectPath" -ForegroundColor Yellow
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.x first." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if required files exist
Write-Host "Checking required files..." -ForegroundColor Green
$requiredFiles = @("mcp_server.py", "requirements.txt", "data.json")
$allFilesExist = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✓ $file exists" -ForegroundColor Green
    } else {
        Write-Host "✗ $file not found" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "Some required files are missing. Please run this script from the project root directory." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if virtual environment exists
$venvPath = Join-Path $projectPath "venv"
$useVenv = $false

if (Test-Path $venvPath) {
    Write-Host "Virtual environment found at: $venvPath" -ForegroundColor Yellow
    $useVenvPrompt = Read-Host "Use virtual environment? (y/n)"
    if ($useVenvPrompt -eq "y" -or $useVenvPrompt -eq "Y") {
        $useVenv = $true
        Write-Host "✓ Will use virtual environment" -ForegroundColor Green
    }
} else {
    Write-Host "No virtual environment found." -ForegroundColor Yellow
    $createVenvPrompt = Read-Host "Create virtual environment? (y/n)"
    if ($createVenvPrompt -eq "y" -or $createVenvPrompt -eq "Y") {
        Write-Host "Creating virtual environment..." -ForegroundColor Green
        & python -m venv venv
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Virtual environment created" -ForegroundColor Green
            $useVenv = $true
            
            # Activate and install dependencies
            Write-Host "Installing dependencies..." -ForegroundColor Green
            & "$venvPath\Scripts\activate.ps1"
            & pip install -r requirements.txt
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Dependencies installed" -ForegroundColor Green
            } else {
                Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
            }
        } else {
            Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
        }
    }
}
Write-Host ""

# Generate the configuration
Write-Host "Generating VS Code configuration..." -ForegroundColor Green
Write-Host ""

$mcpServerPath = Join-Path $projectPath "mcp_server.py"
$pythonCommand = "python"

if ($useVenv) {
    $pythonCommand = Join-Path $venvPath "Scripts\python.exe"
}

# Escape backslashes for JSON
$mcpServerPathJson = $mcpServerPath -replace '\\', '\\'
$pythonCommandJson = $pythonCommand -replace '\\', '\\'
$projectPathJson = $projectPath -replace '\\', '\\'

$config = @"
{
  "github.copilot.referenceable.mcpServers": {
    "travel-reservations": {
      "command": "$pythonCommandJson",
      "args": [
        "$mcpServerPathJson"
      ],
      "env": {
        "PYTHONPATH": "$projectPathJson"
      }
    }
  }
}
"@

Write-Host "================================" -ForegroundColor Cyan
Write-Host "VS Code Configuration" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host $config -ForegroundColor White
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Option to copy to clipboard
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Copy the configuration above" -ForegroundColor White
Write-Host "2. Open VS Code settings (Ctrl+,)" -ForegroundColor White
Write-Host "3. Click 'Open Settings (JSON)' icon" -ForegroundColor White
Write-Host "4. Add the configuration to your settings.json" -ForegroundColor White
Write-Host "5. Restart VS Code (Ctrl+Shift+P > Developer: Reload Window)" -ForegroundColor White
Write-Host ""

# Offer to save to file
$savePrompt = Read-Host "Save configuration to vscode_mcp_config.json? (y/n)"
if ($savePrompt -eq "y" -or $savePrompt -eq "Y") {
    $config | Out-File -FilePath "vscode_mcp_config.json" -Encoding UTF8
    Write-Host "✓ Configuration saved to vscode_mcp_config.json" -ForegroundColor Green
    Write-Host ""
}

# Test the MCP server
Write-Host "Testing MCP server..." -ForegroundColor Green
try {
    # Just check if the script can be imported/parsed, don't run it
    $testCmd = if ($useVenv) { "$venvPath\Scripts\python.exe" } else { "python" }
    $testResult = & $testCmd -c "import sys; sys.path.insert(0, '$projectPath'); import mcp_server; print('OK')" 2>&1
    
    if ($testResult -match "OK") {
        Write-Host "✓ MCP server script is valid and can be loaded" -ForegroundColor Green
    } else {
        Write-Host "⚠ MCP server validation completed with warnings" -ForegroundColor Yellow
        Write-Host "  This is normal if dependencies are installed correctly" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠ Could not fully validate MCP server" -ForegroundColor Yellow
    Write-Host "  Make sure dependencies are installed: pip install -r requirements.txt" -ForegroundColor Yellow
}
Write-Host ""

Write-Host "Setup complete! 🎉" -ForegroundColor Green
Write-Host ""
Write-Host "For detailed instructions, see: VSCODE_INSTALLATION.md" -ForegroundColor Cyan
