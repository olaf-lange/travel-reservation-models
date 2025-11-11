# MCP Tools Quick Reference

## Available Tools

### 1. list_rooms
**Description**: Get all available hotel rooms  
**Parameters**: None  
**Returns**: JSON array of all rooms with details

**Example Usage**:
```
"Show me all available rooms"
"What rooms do you have?"
```

---

### 2. get_room
**Description**: Get detailed information about a specific room  
**Parameters**:
- `room_id` (number, required): Room ID

**Example Usage**:
```
"Tell me about room 2"
"What are the details of room ID 1?"
```

---

### 3. list_reservations
**Description**: Get all current reservations  
**Parameters**: None  
**Returns**: JSON array of all reservations

**Example Usage**:
```
"Show me all reservations"
"What bookings do we have?"
```

---

### 4. get_reservation
**Description**: Get details of a specific reservation  
**Parameters**:
- `reservation_id` (string, required): Reservation ID

**Example Usage**:
```
"Show me reservation abc-123"
"Get details for reservation ID xyz-789"
```

---

### 5. create_reservation
**Description**: Create a new hotel reservation  
**Parameters**:
- `room_id` (number, required): Room to reserve
- `guest_name` (string, required): Guest's full name
- `check_in` (string, required): Check-in date (YYYY-MM-DD)
- `check_out` (string, required): Check-out date (YYYY-MM-DD)

**Example Usage**:
```
"Book room 1 for Jane Smith from 2025-12-01 to 2025-12-05"
"Create a reservation for John Doe in room 2 checking in on 2025-11-15 and checking out on 2025-11-20"
```

---

### 6. cancel_reservation
**Description**: Cancel an existing reservation  
**Parameters**:
- `reservation_id` (string, required): Reservation ID to cancel

**Example Usage**:
```
"Cancel reservation abc-123"
"Remove booking xyz-789"
```

---

### 7. search_available_rooms
**Description**: Search for rooms based on criteria  
**Parameters**:
- `min_availability` (number, optional): Minimum available rooms
- `max_price` (number, optional): Maximum price per night

**Example Usage**:
```
"Find rooms under $150 per night"
"Show me rooms with at least 2 available"
"Search for rooms priced below $200 with availability of 3 or more"
```

---

## Resource Access

### file://data.json
Access the complete hotel data including all rooms and reservations in JSON format.

---

## Error Handling

All tools return errors in JSON format:
```json
{
  "error": "Description of the error"
}
```

Common errors:
- "Room not found"
- "Room not available"
- "Reservation not found"
- "Invalid parameters"

---

## Tips

1. **Date Format**: Always use YYYY-MM-DD format for dates
2. **Room IDs**: Use numeric IDs (1, 2, 3, etc.)
3. **Reservation IDs**: UUIDs returned when creating reservations
4. **Availability**: Check room availability before booking
5. **Price Filter**: Use max_price for budget searches

---

## Configuration

Add to Claude Desktop config:
```json
{
  "mcpServers": {
    "travel-reservations": {
      "command": "python",
      "args": ["x:\\source\\_hackathons\\mcp_travel\\travel-reservation-models\\mcp_server.py"]
    }
  }
}
```

For more details, see [MCP_README.md](MCP_README.md)
