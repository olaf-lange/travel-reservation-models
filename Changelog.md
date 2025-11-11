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