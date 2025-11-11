## [0.3.0] - 2025-11-11

### Added
- MCP (Model Context Protocol) Server (`mcp_server.py`)
  - Programmatic access to reservation system via MCP protocol
  - 7 MCP tools: list_rooms, get_room, list_reservations, get_reservation, create_reservation, cancel_reservation, search_available_rooms
  - Resource access to data.json through MCP protocol
  - Full integration with MCP clients like Claude Desktop
- MCP server documentation (`MCP_README.md`)
  - Detailed tool descriptions and usage examples
  - Client configuration instructions
  - Architecture diagrams
  - Troubleshooting guide
- MCP configuration file (`mcp_config.json`)
  - Sample configuration for MCP clients
- Test script (`test_mcp_server.py`) for MCP server validation
- Usage guide script (`mcp_usage_guide.py`) with interactive examples
- Quick reference guide (`MCP_QUICKREF.md`)
- Project summary document (`PROJECT_SUMMARY.md`)
- VS Code integration (`.vscode/` folder)
  - `settings.json` - MCP server configuration
  - `tasks.json` - Tasks for running MCP and Flask servers
  - `launch.json` - Debug configurations for both servers
  - `README.md` - VS Code configuration documentation
- Added `mcp>=1.0.0` dependency to requirements.txt

### Technical Details
- MCP Server: Python-based stdio server
- Communication: JSON-RPC over stdio
- Shared data storage with Flask web app (data.json)
- Async/await architecture using asyncio
- Full MCP protocol compliance
- VS Code task integration for easy server management

## [0.2.0] - 2025-11-11

### Added
- Flask backend application (`app.py`) with REST API endpoints
  - GET /api/rooms - Retrieve available rooms
  - GET /api/reservations - Retrieve all reservations
  - POST /api/reservations - Create new reservation
  - DELETE /api/reservations/<id> - Cancel reservation
- VueJS frontend application (`src/main.js` and `static/js/main.js`)
  - Room browsing interface with availability status
  - Booking modal for making reservations
  - Reservations management view
  - Form validation and error handling
- HTML template (`templates/index.html`) with Vue 3 and Tailwind CSS via CDN
- Sample data file (`data.json`) with 4 hotel rooms
- Python dependencies file (`requirements.txt`)
- Environment variables example file (`.env.example`)
- Complete project structure following Flask + Vue architecture

### Fixed
- Wrapped Vue template syntax in Jinja2 `{% raw %}` blocks to prevent template syntax conflicts
- Enabled Flask debug mode for automatic reloading during development

### Technical Details
- Backend: Flask 3.0.0 with JSON file-based data storage
- Frontend: Vue 3 (CDN) with Tailwind CSS (CDN)
- UUID-based reservation IDs
- Room availability tracking with automatic updates
- Input validation for dates and required fields

## [0.1.0] - 2025-04-22

### Added
- Initial README, LICENSE, Copilot Instructions, and gitignore