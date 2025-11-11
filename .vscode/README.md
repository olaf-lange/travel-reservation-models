# VS Code Configuration for Travel Reservations MCP Server

This folder contains VS Code-specific configuration for the Travel Reservations project.

## Files

### settings.json
Contains workspace settings including MCP server configuration.

### tasks.json
Defines VS Code tasks for running the servers:
- **Start MCP Server** - Runs the MCP server for integration with MCP clients
- **Start Flask Web Server** - Runs the Flask web application

### launch.json
Debug configurations:
- **Python: MCP Server** - Debug the MCP server
- **Python: Flask** - Debug the Flask web application

## How to Use

### Running the MCP Server

**Option 1: Using VS Code Tasks**
1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
2. Type "Tasks: Run Task"
3. Select "Start MCP Server"

**Option 2: Using Terminal**
```bash
.\\venv\\Scripts\\python.exe mcp_server.py
```

**Option 3: Using Debug**
1. Press `F5` or go to Run and Debug view
2. Select "Python: MCP Server"
3. Click Start Debugging

### Running the Flask Web Server

**Option 1: Using VS Code Tasks**
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "Start Flask Web Server"

**Option 2: Using Terminal**
```bash
.\\venv\\Scripts\\Activate.ps1
$env:FLASK_DEBUG=1
python -m flask run
```

**Option 3: Using Debug**
1. Press `F5`
2. Select "Python: Flask"
3. Click Start Debugging

## MCP Server Integration

The MCP server is configured in `settings.json` and can be used by:

1. **Claude Desktop** - Add the configuration from `mcp_config.json`
2. **Other MCP Clients** - Use the server configuration provided
3. **VS Code Extensions** - Any MCP-compatible VS Code extensions will detect the server

## Notes

- The MCP server runs in stdio mode and waits for JSON-RPC input
- When running, it will appear idle but is actually listening for MCP commands
- The Flask server runs on http://127.0.0.1:5000 by default
- Both servers share the same `data.json` file

## Keyboard Shortcuts

- `F5` - Start debugging with the selected configuration
- `Ctrl+Shift+P` - Command Palette (to access tasks)
- `Ctrl+C` - Stop the currently running task/server

## Troubleshooting

### MCP Server appears idle
This is normal - it's waiting for stdio input from an MCP client.

### Flask server won't start
- Ensure port 5000 is not in use
- Check that virtual environment is activated
- Verify dependencies are installed: `pip install -r requirements.txt`

### Python not found
- Ensure virtual environment is created: `python -m venv venv`
- Path should be: `.\\venv\\Scripts\\python.exe`

## Additional Resources

- Project documentation: `README.md`
- MCP server docs: `MCP_README.md`
- Quick reference: `MCP_QUICKREF.md`
- Project summary: `PROJECT_SUMMARY.md`
