#!/usr/bin/env python3
"""
Quick test script for SAP Groovy MCP Server
"""

import asyncio
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_server import SAPGroovyMCPServer

async def test_server():
    """Test the MCP server functionality."""
    server = SAPGroovyMCPServer()
    
    print("=== Testing SAP Groovy MCP Server ===\n")
    
    # Test list_examples
    print("1. Testing list_examples()...")
    result = await server.list_examples()
    print(result[0].text[:500] + "...\n")
    
    # Test list_examples with tag filter
    print("2. Testing list_examples(tag='beginner')...")
    result = await server.list_examples(tag="beginner")
    print(result[0].text[:500] + "...\n")
    
    # Test get_example
    print("3. Testing get_example('basic')...")
    result = await server.get_example("basic")
    print(result[0].text[:800] + "...\n")
    
    # Test search_examples
    print("4. Testing search_examples('Message')...")
    result = await server.search_examples("Message")
    print(result[0].text[:500] + "...\n")
    
    # Test analyze_script
    print("5. Testing analyze_script('basic')...")
    result = await server.analyze_script("basic")
    print(result[0].text[:500] + "...\n")
    
    # Test compare_examples
    print("6. Testing compare_examples('basic', 'mpl-payload-log')...")
    result = await server.compare_examples("basic", "mpl-payload-log")
    print(result[0].text[:500] + "...\n")
    
    print("=== All tests completed successfully! ===")

if __name__ == "__main__":
    asyncio.run(test_server())
