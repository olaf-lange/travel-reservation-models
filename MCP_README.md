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

#### Claude Desktop Configuration
Add to your Claude Desktop configuration file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "travel-reservations": {
      "command": "python",
      "args": ["x:\\source\\_hackathons\\mcp_travel\\travel-reservation-models\\mcp_server.py"],
      "env": {
        "PYTHONPATH": "x:\\source\\_hackathons\\mcp_travel\\travel-reservation-models"
      }
    }
  }
}
```

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
