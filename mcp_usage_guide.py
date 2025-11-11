#!/usr/bin/env python3
"""
MCP Server Usage Example

This script demonstrates how to integrate the Travel Reservations MCP server
with your MCP client applications.
"""

import json

# Example MCP server configuration for different clients

CLAUDE_DESKTOP_CONFIG = {
    "mcpServers": {
        "travel-reservations": {
            "command": "python",
            "args": ["mcp_server.py"],
            "env": {
                "PYTHONPATH": "x:\\source\\_hackathons\\mcp_travel\\travel-reservation-models"
            }
        }
    }
}

# Example tool usage scenarios
USAGE_EXAMPLES = {
    "List all rooms": {
        "tool": "list_rooms",
        "parameters": {},
        "description": "Get a complete list of all available hotel rooms"
    },
    
    "Get specific room": {
        "tool": "get_room",
        "parameters": {"room_id": 1},
        "description": "Retrieve detailed information about room ID 1"
    },
    
    "Create reservation": {
        "tool": "create_reservation",
        "parameters": {
            "room_id": 1,
            "guest_name": "John Doe",
            "check_in": "2025-12-01",
            "check_out": "2025-12-05"
        },
        "description": "Book room 1 for John Doe from Dec 1-5, 2025"
    },
    
    "Search by price": {
        "tool": "search_available_rooms",
        "parameters": {
            "max_price": 150
        },
        "description": "Find all rooms priced at $150 or less per night"
    },
    
    "List reservations": {
        "tool": "list_reservations",
        "parameters": {},
        "description": "Get all current reservations in the system"
    },
    
    "Cancel reservation": {
        "tool": "cancel_reservation",
        "parameters": {
            "reservation_id": "abc-123-xyz"
        },
        "description": "Cancel the reservation with ID abc-123-xyz"
    }
}


def print_config():
    """Print the MCP server configuration"""
    print("=" * 70)
    print("CLAUDE DESKTOP CONFIGURATION")
    print("=" * 70)
    print("\nAdd this to your Claude Desktop configuration file:")
    print("\nWindows: %APPDATA%\\Claude\\claude_desktop_config.json")
    print("macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("\n" + json.dumps(CLAUDE_DESKTOP_CONFIG, indent=2))
    print("\n")


def print_usage_examples():
    """Print usage examples"""
    print("=" * 70)
    print("USAGE EXAMPLES")
    print("=" * 70)
    print("\nOnce configured, you can use natural language with your MCP client:")
    print()
    
    for scenario, details in USAGE_EXAMPLES.items():
        print(f"\n📌 {scenario}")
        print(f"   Tool: {details['tool']}")
        print(f"   Description: {details['description']}")
        if details['parameters']:
            print(f"   Parameters: {json.dumps(details['parameters'], indent=6)}")
        print()


def print_natural_language_examples():
    """Print natural language query examples"""
    print("=" * 70)
    print("NATURAL LANGUAGE EXAMPLES")
    print("=" * 70)
    print("\nYou can interact using natural language like:")
    print()
    
    examples = [
        "Show me all available rooms",
        "What's the price of room 2?",
        "Book room 1 for Alice Johnson from November 15 to November 20, 2025",
        "List all current reservations",
        "Find rooms that cost less than $200 per night",
        "Cancel my reservation ID abc-123",
        "Which rooms have at least 3 units available?",
        "Tell me about the Executive Suite",
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"  {i}. \"{example}\"")
    
    print()


def main():
    """Main function to display usage information"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "TRAVEL RESERVATIONS MCP SERVER" + " " * 23 + "║")
    print("║" + " " * 22 + "Usage Guide" + " " * 35 + "║")
    print("╚" + "=" * 68 + "╝")
    print("\n")
    
    print_config()
    print_usage_examples()
    print_natural_language_examples()
    
    print("=" * 70)
    print("ADDITIONAL RESOURCES")
    print("=" * 70)
    print("\n📖 Full Documentation: MCP_README.md")
    print("📋 Quick Reference: MCP_QUICKREF.md")
    print("🔧 Configuration: mcp_config.json")
    print("🌐 Web UI: Run 'python app.py' and visit http://127.0.0.1:5000")
    print("\n" + "=" * 70)
    print()


if __name__ == "__main__":
    main()
