# Travel Reservations MCP Server

This MCP (Model Context Protocol) server provides programmatic access to the travel reservations system functionality through standardized MCP tools and resources.

## Features

The MCP server exposes the following capabilities:

### Resources
- **Hotel Data** (`file://data.json`): Access to current rooms and reservations data

### Tools

#### 1. `list_rooms`
Get a list of all available hotel rooms with their details and availability.
- **Parameters**: None
- **Returns**: JSON array of room objects

#### 2. `get_room`
Get detailed information about a specific room by ID.
- **Parameters**:
  - `room_id` (number, required): The ID of the room to retrieve
- **Returns**: JSON object with room details

#### 3. `list_reservations`
Get a list of all current reservations.
- **Parameters**: None
- **Returns**: JSON array of reservation objects

#### 4. `get_reservation`
Get detailed information about a specific reservation by ID.
- **Parameters**:
  - `reservation_id` (string, required): The ID of the reservation to retrieve
- **Returns**: JSON object with reservation details

#### 5. `create_reservation`
Create a new hotel reservation for a guest.
- **Parameters**:
  - `room_id` (number, required): The ID of the room to reserve
  - `guest_name` (string, required): Full name of the guest
  - `check_in` (string, required): Check-in date in YYYY-MM-DD format
  - `check_out` (string, required): Check-out date in YYYY-MM-DD format
- **Returns**: JSON object with reservation details and success status

#### 6. `cancel_reservation`
Cancel an existing reservation and restore room availability.
- **Parameters**:
  - `reservation_id` (string, required): The ID of the reservation to cancel
- **Returns**: JSON object with success status

#### 7. `search_available_rooms`
Search for available rooms based on criteria.
- **Parameters**:
  - `min_availability` (number, optional): Minimum number of available rooms
  - `max_price` (number, optional): Maximum price per night
- **Returns**: JSON object with array of matching rooms

## Installation

1. **Install MCP SDK**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify the MCP server**:
   ```bash
   python mcp_server.py
   ```

## Running the MCP Server

### Standalone Mode
Run the MCP server directly:
```bash
python mcp_server.py
```

The server communicates via stdio (standard input/output) following the MCP protocol.

### Integration with MCP Clients

#### VS Code Configuration

To install and use the travel-reservation-models MCP server in VS Code with GitHub Copilot, follow these steps:

##### Prerequisites
- VS Code installed
- GitHub Copilot extension installed
- Python 3.x installed and accessible from command line

##### Installation Steps

1. **Open VS Code Settings**:
   - Press `Ctrl+,` (Windows/Linux) or `Cmd+,` (macOS)
   - Or navigate to File > Preferences > Settings

2. **Configure MCP Server**:
   - Search for "MCP" in the settings search bar
   - Look for "GitHub > Copilot > Referenceable: Mcp Servers"
   - Click "Edit in settings.json"

3. **Add Server Configuration**:
   Add the following configuration to your `settings.json`:

   **Windows**:
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

   **macOS/Linux**:
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

   **Important**: Replace the paths with your actual project location.

4. **Using Virtual Environment (Optional but Recommended)**:
   If you're using a Python virtual environment, update the configuration:

   **Windows**:
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

   **macOS/Linux**:
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

5. **Restart VS Code**:
   - Close and reopen VS Code to apply the changes
   - Or use the command palette (`Ctrl+Shift+P`/`Cmd+Shift+P`) and run "Developer: Reload Window"

##### Verification

1. **Check Server Status**:
   - Open GitHub Copilot Chat in VS Code
   - Type `@workspace` and you should see the travel-reservations MCP server available

2. **Test the Connection**:
   Try asking Copilot:
   - "Show me all available rooms from the travel reservations server"
   - "List current reservations"

##### Troubleshooting VS Code Integration

**Server not showing up**:
- Verify Python is in your system PATH: `python --version` or `python3 --version`
- Check that the paths in settings.json are absolute and correct
- Ensure `mcp_server.py` has the correct permissions
- Check VS Code's Output panel (View > Output) and select "GitHub Copilot" from the dropdown

**Permission errors**:
- On Windows, run VS Code as administrator if needed
- On macOS/Linux, ensure the script has execute permissions: `chmod +x mcp_server.py`

**Import errors**:
- Verify all dependencies are installed: `pip install -r requirements.txt`
- If using a virtual environment, ensure it's activated or use the full path to the venv Python executable

**Path issues on Windows**:
- Use double backslashes `\\` or forward slashes `/` in JSON paths
- Example: `"Y:\\path\\to\\file"` or `"Y:/path/to/file"`

#### Claude Desktop Configuration
Add to your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "travel-reservations": {
      "command": "python",
      "args": ["Y:\\source\\_hackathons\\mcp_travel\\travel-reservation-models\\mcp_server.py"],
      "env": {
        "PYTHONPATH": "Y:\\source\\_hackathons\\mcp_travel\\travel-reservation-models"
      }
    }
  }
}
```

**Note**: Update the path to match your actual installation directory.

#### Other MCP Clients
Use the provided `mcp_config.json` as a reference for configuring other MCP clients.

## Usage Examples

Once connected through an MCP client (like Claude Desktop), you can use natural language to interact with the reservation system:

- "Show me all available rooms"
- "Create a reservation for John Doe in room 1 from 2025-12-01 to 2025-12-05"
- "List all current reservations"
- "Cancel reservation with ID abc-123"
- "Find rooms under $150 per night"

## Architecture

```
┌─────────────────┐
│   MCP Client    │
│ (Claude Desktop)│
└────────┬────────┘
         │ stdio
         │ (MCP Protocol)
┌────────▼────────┐
│   mcp_server.py │
│   MCP Server    │
└────────┬────────┘
         │
┌────────▼────────┐
│   data.json     │
│   Data Storage  │
└─────────────────┘
```

## Development

The MCP server shares the same data file (`data.json`) with the Flask web application, allowing seamless integration between the web UI and MCP interface.

### File Structure
```
mcp_server.py      # MCP server implementation
mcp_config.json    # MCP client configuration
MCP_README.md      # This file
data.json          # Shared data storage
```

## Error Handling

The server provides detailed error messages for:
- Room not found
- Room not available
- Reservation not found
- Invalid parameters
- Data validation errors

All errors are returned as JSON objects with an `error` field.

## Security Considerations

- The MCP server operates with local file system access
- No authentication is currently implemented (suitable for local/development use)
- Data is stored in plain JSON format
- For production use, consider adding:
  - Authentication and authorization
  - Database backend
  - Input sanitization
  - Rate limiting

## Troubleshooting

### Server won't start
- Ensure Python 3.x is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check that `data.json` exists and is valid JSON

### MCP client can't connect
- Verify the path to `mcp_server.py` in the configuration
- Check that Python is in your system PATH
- Ensure virtual environment is activated if using one

### Data not updating
- Confirm `data.json` file permissions
- Check for file locking issues if both web app and MCP server are running simultaneously

## License

This project is licensed under the MIT License. See the LICENSE file for details.
