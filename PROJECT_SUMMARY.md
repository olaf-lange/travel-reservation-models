# Travel Reservations MCP Server - Project Summary

## 🎯 Overview

This project provides a complete hotel reservation management system with **three interfaces**:

1. **Web Application** (Flask + Vue.js) - Interactive web UI
2. **REST API** (Flask) - HTTP-based programmatic access
3. **MCP Server** (Model Context Protocol) - AI assistant integration

## 📁 Project Structure

```
travel-reservation-models/
├── app.py                      # Flask web application & REST API
├── mcp_server.py               # MCP server implementation
├── data.json                   # Shared data storage (rooms & reservations)
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html              # Vue.js web interface
├── static/js/
│   └── main.js                 # Vue.js application code
├── src/
│   └── main.js                 # Vue.js source (copied to static)
├── .vscode/
│   └── settings.json.example   # VS Code MCP configuration example
├── README.md                   # Main project documentation
├── MCP_README.md               # MCP server detailed documentation
├── VSCODE_INSTALLATION.md      # VS Code setup guide (NEW)
├── MCP_QUICKREF.md             # Quick reference for MCP tools
├── mcp_config.json             # MCP client configuration sample
├── mcp_usage_guide.py          # Interactive usage guide
├── test_mcp_server.py          # MCP server test script
├── setup_vscode_mcp.ps1        # Windows setup script (NEW)
├── setup_vscode_mcp.sh         # macOS/Linux setup script (NEW)
├── Changelog.md                # Version history
├── .env.example                # Environment variables template
└── LICENSE                     # MIT License

```

## 🚀 Getting Started

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Web Application

```bash
# Development mode with auto-reload
$env:FLASK_DEBUG=1
python -m flask run

# Visit: http://127.0.0.1:5000
```

### 3. Run the MCP Server

```bash
# The MCP server runs via stdio for MCP clients
python mcp_server.py

# For configuration help:
python mcp_usage_guide.py
```

## 🔧 MCP Server Features

### Available Tools (7 total)

1. **list_rooms** - Get all available hotel rooms
2. **get_room** - Get specific room details by ID
3. **list_reservations** - Get all reservations
4. **get_reservation** - Get specific reservation by ID
5. **create_reservation** - Book a new reservation
6. **cancel_reservation** - Cancel existing reservation
7. **search_available_rooms** - Search by criteria (price, availability)

### Resource Access

- **file://data.json** - Direct access to hotel data

## 💻 Usage Examples

### Web Application
1. Navigate to http://127.0.0.1:5000
2. Browse available rooms
3. Click "Book Now" on any room
4. Fill in guest details and dates
5. View/manage reservations in the "My Reservations" tab

### REST API

```bash
# List rooms
curl http://127.0.0.1:5000/api/rooms

# Create reservation
curl -X POST http://127.0.0.1:5000/api/reservations \
  -H "Content-Type: application/json" \
  -d '{"roomId": 1, "guestName": "John Doe", "checkIn": "2025-12-01", "checkOut": "2025-12-05"}'

# List reservations
curl http://127.0.0.1:5000/api/reservations

# Cancel reservation
curl -X DELETE http://127.0.0.1:5000/api/reservations/{id}
```

### MCP Server (via Claude Desktop or other MCP clients)

Natural language examples:
- "Show me all available rooms"
- "Book room 1 for Alice from December 1-5, 2025"
- "Find rooms under $150 per night"
- "List all reservations"
- "Cancel reservation abc-123"

## 🔌 MCP Client Integration

### VS Code with GitHub Copilot

**Quick Setup**:
```powershell
# Windows
.\setup_vscode_mcp.ps1

# macOS/Linux
chmod +x setup_vscode_mcp.sh
./setup_vscode_mcp.sh
```

**Manual Setup**: See detailed instructions in [VSCODE_INSTALLATION.md](VSCODE_INSTALLATION.md)

**Example Configuration** (add to VS Code `settings.json`):
```json
{
  "github.copilot.referenceable.mcpServers": {
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

### Claude Desktop

1. **Locate Configuration File**:
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add Server Configuration**:
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

3. **Restart Claude Desktop**

4. **Verify Connection**: Look for the travel-reservations server in the available tools

## 📊 Data Model

### Room Object
```json
{
  "id": 1,
  "name": "Standard Queen",
  "description": "Comfortable room with queen-size bed",
  "price": 99,
  "availability": 5
}
```

### Reservation Object
```json
{
  "id": "uuid-string",
  "roomId": 1,
  "guestName": "John Doe",
  "checkIn": "2025-12-01",
  "checkOut": "2025-12-05",
  "createdAt": "2025-11-11T20:00:00"
}
```

## 🛠️ Technology Stack

- **Backend**: Python 3.x, Flask 3.0.0
- **Frontend**: Vue.js 3 (CDN), Tailwind CSS (CDN)
- **MCP**: Python MCP SDK 1.21.0
- **Data**: JSON file-based storage
- **Communication**: HTTP REST API, MCP stdio protocol

## 📚 Documentation

- **README.md** - Main project overview and setup
- **MCP_README.md** - Complete MCP server documentation
- **MCP_QUICKREF.md** - Quick reference for all MCP tools
- **Changelog.md** - Version history and changes

## 🧪 Testing

```bash
# Test the web application
# 1. Start the Flask server
python -m flask run

# 2. Visit http://127.0.0.1:5000 in browser

# Test the MCP server
# 1. Configure in Claude Desktop (see above)
# 2. Restart Claude Desktop
# 3. Try natural language queries
```

## 🔐 Security Notes

⚠️ **This is a development/demo application**

- No authentication implemented
- Data stored in plain JSON
- Suitable for local development and testing
- For production use, add:
  - User authentication
  - Database backend (PostgreSQL, MySQL)
  - Input sanitization
  - Rate limiting
  - HTTPS/TLS

## 🐛 Troubleshooting

### Web App won't start
- Check Python version: `python --version` (3.x required)
- Verify dependencies: `pip install -r requirements.txt`
- Check port 5000 is available

### MCP Server issues
- Verify MCP SDK installed: `pip show mcp`
- Check configuration path in Claude Desktop config
- Ensure Python is in system PATH
- Check `data.json` exists and is valid JSON

### Data not updating
- Stop both web app and MCP server
- Verify `data.json` file permissions
- Restart services one at a time

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

- Issues: File on GitHub repository
- Documentation: See README.md and MCP_README.md
- Examples: Run `python mcp_usage_guide.py`

---

**Version**: 0.3.0  
**Last Updated**: November 11, 2025  
**Author**: Travel Reservations Team
