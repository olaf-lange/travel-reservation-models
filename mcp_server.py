"""
Travel Reservations MCP Server
Provides MCP (Model Context Protocol) interface for hotel reservation management
"""

import json
import os
import uuid
from datetime import datetime
from typing import Any
import asyncio

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

# Constants
DATA_FILE = 'data.json'
SERVER_NAME = "travel-reservations-server"
SERVER_VERSION = "0.1.0"

# Initialize MCP server
app = Server(SERVER_NAME)


def load_data() -> dict:
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"rooms": [], "reservations": []}


def save_data(data: dict) -> None:
    """Save data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


@app.list_resources()
async def handle_list_resources() -> list[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="file://data.json",
            name="Hotel Data",
            description="Current hotel rooms and reservations data",
            mimeType="application/json",
        )
    ]


@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read resource content"""
    if uri == "file://data.json":
        data = load_data()
        return json.dumps(data, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="list_rooms",
            description="Get a list of all available hotel rooms with their details and availability",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_room",
            description="Get detailed information about a specific room by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "number",
                        "description": "The ID of the room to retrieve",
                    },
                },
                "required": ["room_id"],
            },
        ),
        Tool(
            name="list_reservations",
            description="Get a list of all current reservations",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_reservation",
            description="Get detailed information about a specific reservation by ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "reservation_id": {
                        "type": "string",
                        "description": "The ID of the reservation to retrieve",
                    },
                },
                "required": ["reservation_id"],
            },
        ),
        Tool(
            name="create_reservation",
            description="Create a new hotel reservation for a guest",
            inputSchema={
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "number",
                        "description": "The ID of the room to reserve",
                    },
                    "guest_name": {
                        "type": "string",
                        "description": "Full name of the guest",
                    },
                    "check_in": {
                        "type": "string",
                        "description": "Check-in date in YYYY-MM-DD format",
                    },
                    "check_out": {
                        "type": "string",
                        "description": "Check-out date in YYYY-MM-DD format",
                    },
                },
                "required": ["room_id", "guest_name", "check_in", "check_out"],
            },
        ),
        Tool(
            name="cancel_reservation",
            description="Cancel an existing reservation and restore room availability",
            inputSchema={
                "type": "object",
                "properties": {
                    "reservation_id": {
                        "type": "string",
                        "description": "The ID of the reservation to cancel",
                    },
                },
                "required": ["reservation_id"],
            },
        ),
        Tool(
            name="search_available_rooms",
            description="Search for available rooms based on criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "min_availability": {
                        "type": "number",
                        "description": "Minimum number of available rooms (optional)",
                    },
                    "max_price": {
                        "type": "number",
                        "description": "Maximum price per night (optional)",
                    },
                },
                "required": [],
            },
        ),
    ]


@app.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool execution"""
    
    try:
        if name == "list_rooms":
            data = load_data()
            rooms = data.get('rooms', [])
            return [
                TextContent(
                    type="text",
                    text=json.dumps(rooms, indent=2)
                )
            ]
        
        elif name == "get_room":
            room_id = arguments.get("room_id")
            data = load_data()
            room = next((r for r in data['rooms'] if r['id'] == room_id), None)
            
            if not room:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"error": "Room not found"}, indent=2)
                    )
                ]
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(room, indent=2)
                )
            ]
        
        elif name == "list_reservations":
            data = load_data()
            reservations = data.get('reservations', [])
            return [
                TextContent(
                    type="text",
                    text=json.dumps(reservations, indent=2)
                )
            ]
        
        elif name == "get_reservation":
            reservation_id = arguments.get("reservation_id")
            data = load_data()
            reservation = next(
                (r for r in data['reservations'] if r['id'] == reservation_id),
                None
            )
            
            if not reservation:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"error": "Reservation not found"}, indent=2)
                    )
                ]
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(reservation, indent=2)
                )
            ]
        
        elif name == "create_reservation":
            data = load_data()
            room_id = arguments.get("room_id")
            guest_name = arguments.get("guest_name")
            check_in = arguments.get("check_in")
            check_out = arguments.get("check_out")
            
            # Validate room exists and is available
            room = next((r for r in data['rooms'] if r['id'] == room_id), None)
            
            if not room:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"error": "Room not found"}, indent=2)
                    )
                ]
            
            if room['availability'] <= 0:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"error": "Room not available"}, indent=2)
                    )
                ]
            
            # Create reservation
            reservation = {
                'id': str(uuid.uuid4()),
                'roomId': room_id,
                'guestName': guest_name,
                'checkIn': check_in,
                'checkOut': check_out,
                'createdAt': datetime.now().isoformat()
            }
            
            # Update room availability
            room['availability'] -= 1
            
            # Add reservation
            data['reservations'].append(reservation)
            save_data(data)
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "success": True,
                        "reservation": reservation,
                        "message": f"Reservation created successfully for {guest_name}"
                    }, indent=2)
                )
            ]
        
        elif name == "cancel_reservation":
            data = load_data()
            reservation_id = arguments.get("reservation_id")
            
            # Find reservation
            reservation = next(
                (r for r in data['reservations'] if r['id'] == reservation_id),
                None
            )
            
            if not reservation:
                return [
                    TextContent(
                        type="text",
                        text=json.dumps({"error": "Reservation not found"}, indent=2)
                    )
                ]
            
            # Update room availability
            room = next((r for r in data['rooms'] if r['id'] == reservation['roomId']), None)
            if room:
                room['availability'] += 1
            
            # Remove reservation
            data['reservations'] = [
                r for r in data['reservations'] if r['id'] != reservation_id
            ]
            save_data(data)
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "success": True,
                        "message": "Reservation cancelled successfully"
                    }, indent=2)
                )
            ]
        
        elif name == "search_available_rooms":
            data = load_data()
            rooms = data.get('rooms', [])
            
            min_availability = arguments.get("min_availability", 1)
            max_price = arguments.get("max_price", float('inf'))
            
            # Filter rooms
            available_rooms = [
                r for r in rooms
                if r['availability'] >= min_availability and r.get('price', 0) <= max_price
            ]
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "total_found": len(available_rooms),
                        "rooms": available_rooms
                    }, indent=2)
                )
            ]
        
        else:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
                )
            ]
    
    except Exception as e:
        return [
            TextContent(
                type="text",
                text=json.dumps({"error": str(e)}, indent=2)
            )
        ]


async def main():
    """Main entry point for the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version=SERVER_VERSION,
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
