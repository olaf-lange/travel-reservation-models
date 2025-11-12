# Installing Travel Reservations MCP Server in VS Code

This guide provides step-by-step instructions for installing and configuring the travel-reservation-models MCP server in Visual Studio Code with GitHub Copilot.

## Prerequisites

Before you begin, ensure you have:

- ✅ Visual Studio Code installed
- ✅ GitHub Copilot extension installed and activated
- ✅ Python 3.x installed (`python --version` should work in terminal)
- ✅ MCP dependencies installed (see [Installation](#installation) below)

## Installation

### Quick Setup (Recommended)

We provide automated setup scripts to help you configure the MCP server:

**Windows (PowerShell)**:
```powershell
.\setup_vscode_mcp.ps1
```

**macOS/Linux (Bash)**:
```bash
chmod +x setup_vscode_mcp.sh
./setup_vscode_mcp.sh
```

These scripts will:
- ✅ Check Python installation
- ✅ Verify required files
- ✅ Create/detect virtual environment
- ✅ Generate the VS Code configuration
- ✅ Save configuration to a file
- ✅ Test the MCP server

After running the script, copy the generated configuration to your VS Code `settings.json`.

---

### Manual Setup

If you prefer to set up manually or the automated script doesn't work:

### Step 1: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
# If using a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Verify MCP Server Works

Test that the MCP server runs correctly:

```bash
python mcp_server.py
```

The server should start without errors. Press `Ctrl+C` to stop it.

### Step 3: Configure VS Code

1. **Open VS Code Settings**:
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (macOS)
   - Or: File → Preferences → Settings

2. **Open settings.json**:
   - Click the "Open Settings (JSON)" icon in the top-right corner
   - Or press `Ctrl+Shift+P` and search for "Preferences: Open User Settings (JSON)"

3. **Add MCP Server Configuration**:

   Add this configuration to your `settings.json` file:

   #### For Windows:
   ```json
   {
     "github.copilot.referenceable.mcpServers": {
       "travel-reservations": {
         "command": "python",
         "args": [
           "Y:\\source\\_hackathons\\mcp_travel\\travel-reservation-models\\mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "Y:\\source\\_hackathons\\mcp_travel\\travel-reservation-models"
         }
       }
     }
   }
   ```

   #### For macOS/Linux:
   ```json
   {
     "github.copilot.referenceable.mcpServers": {
       "travel-reservations": {
         "command": "python3",
         "args": [
           "/path/to/your/travel-reservation-models/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "/path/to/your/travel-reservation-models"
         }
       }
     }
   }
   ```

   **⚠️ Important**: Replace the paths with your actual project location!

4. **Using Virtual Environment** (if applicable):

   If you're using a Python virtual environment, use the Python executable from your venv:

   #### Windows with venv:
   ```json
   {
     "github.copilot.referenceable.mcpServers": {
       "travel-reservations": {
         "command": "Y:\\source\\_hackathons\\mcp_travel\\travel-reservation-models\\venv\\Scripts\\python.exe",
         "args": [
           "Y:\\source\\_hackathons\\mcp_travel\\travel-reservation-models\\mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "Y:\\source\\_hackathons\\mcp_travel\\travel-reservation-models"
         }
       }
     }
   }
   ```

   #### macOS/Linux with venv:
   ```json
   {
     "github.copilot.referenceable.mcpServers": {
       "travel-reservations": {
         "command": "/path/to/your/travel-reservation-models/venv/bin/python",
         "args": [
           "/path/to/your/travel-reservation-models/mcp_server.py"
         ],
         "env": {
           "PYTHONPATH": "/path/to/your/travel-reservation-models"
         }
       }
     }
   }
   ```

### Step 4: Restart VS Code

- **Option 1**: Close and reopen VS Code
- **Option 2**: Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS) → "Developer: Reload Window"

## Verification

### Check if the Server is Running

1. Open **GitHub Copilot Chat** in VS Code (click the chat icon in the sidebar)
2. Type `@workspace` and you should see suggestions including tools from the travel-reservations server
3. Try asking: "Show me all available rooms"

### Test MCP Tools

Try these example prompts in Copilot Chat:

```
@workspace List all available hotel rooms

@workspace Create a reservation for Jane Smith in room 2 from 2025-12-15 to 2025-12-20

@workspace Show me all current reservations

@workspace Find rooms under $150 per night

@workspace Cancel reservation with ID [reservation-id]
```

## Troubleshooting

### 🔴 Server Not Showing Up

**Problem**: MCP server doesn't appear in Copilot's available tools

**Solutions**:
- Verify Python is accessible: Open terminal and run `python --version` or `python3 --version`
- Check paths in `settings.json` are **absolute** and **correct**
- Ensure forward slashes `/` or escaped backslashes `\\` in Windows paths
- Check VS Code Output panel:
  - View → Output
  - Select "GitHub Copilot" from the dropdown
  - Look for error messages

### 🔴 Permission Errors

**Problem**: "Permission denied" or "Access denied" errors

**Solutions**:
- **Windows**: Try running VS Code as administrator
- **macOS/Linux**: Make script executable: `chmod +x mcp_server.py`
- Check file permissions on `mcp_server.py` and `data.json`

### 🔴 Import Errors / Module Not Found

**Problem**: `ModuleNotFoundError` for `mcp`, `flask`, etc.

**Solutions**:
- Verify dependencies are installed: `pip install -r requirements.txt`
- If using a virtual environment:
  - Make sure it's activated when testing
  - Use the **full path** to the venv Python executable in `settings.json`
  - Example: `Y:\\...\\venv\\Scripts\\python.exe` (Windows) or `/path/to/venv/bin/python` (macOS/Linux)

### 🔴 Path Issues on Windows

**Problem**: JSON parse errors or path not found

**Solutions**:
- Use **double backslashes**: `"Y:\\path\\to\\file"` ✅
- Or use **forward slashes**: `"Y:/path/to/file"` ✅
- Don't use single backslashes: `"Y:\path\to\file"` ❌

### 🔴 Server Starts But No Response

**Problem**: Server appears to run but doesn't respond to requests

**Solutions**:
- Check `data.json` exists and contains valid JSON
- Verify `data.json` file permissions (read/write access)
- Check for file locking if Flask app is also running
- Look for errors in VS Code's Output panel

### 🔴 VS Code Freezes or Hangs

**Problem**: VS Code becomes unresponsive when using MCP server

**Solutions**:
- Restart VS Code
- Check if `data.json` is corrupted
- Verify the MCP server script runs without errors standalone
- Check system resources (CPU/Memory)

## Configuration Reference

### Minimal Configuration

```json
{
  "github.copilot.referenceable.mcpServers": {
    "travel-reservations": {
      "command": "python",
      "args": ["<absolute-path-to-mcp_server.py>"]
    }
  }
}
```

### Full Configuration with Environment Variables

```json
{
  "github.copilot.referenceable.mcpServers": {
    "travel-reservations": {
      "command": "python",
      "args": ["<absolute-path-to-mcp_server.py>"],
      "env": {
        "PYTHONPATH": "<absolute-path-to-project-directory>",
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Configuration with Working Directory

```json
{
  "github.copilot.referenceable.mcpServers": {
    "travel-reservations": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "<absolute-path-to-project-directory>",
      "env": {
        "PYTHONPATH": "<absolute-path-to-project-directory>"
      }
    }
  }
}
```

## Usage Examples

Once configured, you can use natural language with GitHub Copilot to interact with the reservation system:

### Viewing Data
- "Show me all hotel rooms"
- "What rooms are available?"
- "List all reservations"
- "Show me details for room 1"

### Making Reservations
- "Create a reservation for John Doe in room 3 from 2025-12-01 to 2025-12-05"
- "Book room 2 for Sarah Johnson, check-in 2026-01-10, check-out 2026-01-15"

### Searching
- "Find rooms under $200 per night"
- "Show available rooms with at least 3 rooms available"
- "Search for rooms with availability and max price $150"

### Managing Reservations
- "Cancel reservation abc-123"
- "Remove the reservation for guest John Doe"

## Alternative: Workspace-Specific Configuration

You can also configure the MCP server per-workspace by adding the configuration to `.vscode/settings.json` in your project directory:

```json
{
  "github.copilot.referenceable.mcpServers": {
    "travel-reservations": {
      "command": "python",
      "args": ["${workspaceFolder}/mcp_server.py"],
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  }
}
```

This uses VS Code's `${workspaceFolder}` variable for relative paths.

## Additional Resources

- [MCP Documentation](MCP_README.md) - Full MCP server documentation
- [Project README](README.md) - Main project documentation
- [MCP Quick Reference](MCP_QUICKREF.md) - Quick reference guide
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

## Support

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review the [MCP_README.md](MCP_README.md) for general MCP information
3. Verify your Python and VS Code installations
4. Check VS Code's Output panel for detailed error messages

## License

This project is licensed under the MIT License. See the LICENSE file for details.
