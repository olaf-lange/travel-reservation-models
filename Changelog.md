# Changelog

All notable changes to the Travel Reservations project will be documented in this file.

## [0.6.0] - 2025-11-12

### Added
- **MCP Server: update_reservation tool** (Issue #4)
  - New `update_reservation` MCP tool for modifying existing reservations
  - Support for partial updates (all fields optional except reservation_id)
  - Update guest name, check-in date, check-out date, and/or room ID
  - Comprehensive field validation:
    - Guest name (cannot be empty)
    - Room ID (must exist and be available when changing)
    - Check-in/check-out dates (format and logic validation)
  - Room availability management when changing rooms:
    - Automatically restores availability to old room (+1)
    - Reduces availability on new room (-1)
    - Validates new room has availability before switching
    - No changes when keeping the same room
  - Preserves immutable fields:
    - Reservation ID remains constant
    - Creation timestamp never changes
  - AI-optimized response format with success/error messages
  
- **Comprehensive test suite for MCP server** (`test_mcp_server.py`)
  - 27 pytest-based async test cases covering all scenarios:
    - 6 successful update tests (happy paths)
    - 8 validation error tests (error handling)
    - 4 room availability tests (business logic)
    - 4 data integrity tests (data consistency)
    - 3 edge case tests (boundary conditions)
    - 2 additional validation tests
  - All tests passing (27/27) ✅
  - Test coverage: 57% overall (focused on new tool)
  - Uses pytest-asyncio for async test execution
  - Automatic test data setup and teardown

### Changed
- Updated `mcp_server.py`:
  - Added `update_reservation` tool to `handle_list_tools()`
  - Implemented handler logic in `handle_call_tool()`
  - Enhanced date validation with datetime parsing
  - Improved error messages for AI assistant context
- Updated `requirements.txt`:
  - Added `pytest-asyncio>=0.21.0` for async testing support

### Technical Details
- Update tool supports partial updates (all fields optional except reservation_id)
- Validates dates in YYYY-MM-DD format using datetime.strptime
- Ensures check-out date is always after check-in date
- Returns structured JSON with success flag, reservation object, and message
- Consistent behavior with Flask API PUT endpoint
- Thread-safe data persistence to JSON file

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