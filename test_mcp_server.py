"""
Test script for the MCP server
This script sends test commands to the MCP server to verify functionality
"""

import json
import subprocess
import sys

def send_jsonrpc_request(method, params=None):
    """Send a JSON-RPC request to the MCP server"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    return json.dumps(request)

def test_mcp_server():
    """Test the MCP server with sample requests"""
    
    # Start the MCP server process
    process = subprocess.Popen(
        ['python', 'mcp_server.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Test 1: Initialize
        print("Testing MCP Server...")
        print("-" * 50)
        
        init_request = send_jsonrpc_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        print("Sending initialize request...")
        process.stdin.write(init_request + "\n")
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        print("Response:", response)
        
        # Test 2: List tools
        list_tools_request = send_jsonrpc_request("tools/list")
        print("\nSending tools/list request...")
        process.stdin.write(list_tools_request + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print("Response:", response)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    print("MCP Server Test Script")
    print("=" * 50)
    print("\nNote: The MCP server is designed to be used with MCP clients")
    print("like Claude Desktop, not directly from command line.")
    print("\nFor proper testing, configure the server in an MCP client.")
    print("\nServer configuration is available in mcp_config.json")
    print("See MCP_README.md for full instructions.")
    print("=" * 50)
