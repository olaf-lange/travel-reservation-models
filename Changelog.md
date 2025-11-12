# Changelog

All notable changes to the Travel Reservations project will be documented in this file.

## [0.4.0] - 2025-11-12

### Added
- **VS Code MCP Server Installation Documentation**
  - Comprehensive installation guide (`VSCODE_INSTALLATION.md`)
    - Prerequisites and dependency installation
    - Step-by-step VS Code configuration instructions
    - Virtual environment setup guidance
    - Detailed troubleshooting section
    - Configuration reference examples
    - Usage examples and verification steps
  - Automated setup scripts
    - `setup_vscode_mcp.ps1` - PowerShell script for Windows
    - `setup_vscode_mcp.sh` - Bash script for macOS/Linux
    - Interactive setup with Python checking, venv detection/creation
    - Automatic configuration generation
    - MCP server validation (non-blocking)
  - Example VS Code settings (`.vscode/settings.json.example`)
    - Multiple configuration options (absolute paths, workspace variables, venv)
    - Platform-specific examples (Windows, macOS, Linux)
    - Commented alternatives for different setups

### Changed
- Updated `MCP_README.md` with VS Code configuration section
  - Added VS Code as primary integration option
  - Detailed Windows and macOS/Linux setup instructions
  - Virtual environment configuration examples
  - VS Code-specific troubleshooting tips
- Updated `README.md` with documentation links
  - Added links to VSCODE_INSTALLATION.md
  - Reorganized documentation section
  - Added MCP technologies to tech stack
- Updated `PROJECT_SUMMARY.md`
  - Added new files to project structure
  - Added VS Code integration section with quick setup commands
  - Updated MCP client integration documentation
- Updated `mcp_config.json` with corrected paths
  - Changed from X: drive to Y: drive paths
  - Reference configuration for other MCP clients

### Fixed
- **Fixed hanging issue in `test_mcp_server.py`** (#issue)
  - Rewrote test script to properly handle stdio-based MCP server
  - Added timeout handling for MCP protocol tests
  - Improved test suite with 5 comprehensive tests:
    1. Module import validation
    2. Dependency checking
    3. Data file validation
    4. Python syntax verification
    5. MCP protocol communication (with timeout)
  - Test now completes successfully without hanging
  - Added helpful error messages and next steps
- **Fixed hanging issue in setup scripts**
  - `setup_vscode_mcp.ps1` and `setup_vscode_mcp.sh` now validate server without running it
  - Changed from execution test to import validation
  - Scripts complete in seconds instead of hanging indefinitely

### Documentation Improvements
- Comprehensive VS Code installation documentation with:
  - Quick setup scripts for automated configuration
  - Manual setup instructions for advanced users
  - Troubleshooting guide covering common issues
  - Configuration variants for different environments
  - Verification and testing procedures
  - Example usage patterns for GitHub Copilot integration

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