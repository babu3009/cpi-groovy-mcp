# Testing Guide for SAP Groovy MCP Server

## Quick Start Testing

### Option 1: Run the Test Script (Recommended)

The easiest way to test all functionality:

```bash
# Activate your conda environment
conda activate cpimcp

# Navigate to the project directory
cd c:\Code\sap\cpi-groovy-examples.worktrees\copilot-worktree-2026-01-13T12-40-20

# Run the test script
python test_server.py
```

**Expected Output:**
```
=== Testing SAP Groovy MCP Server ===

1. Testing list_examples()...
# SAP CPI Groovy Examples
[Lists all examples with metadata]

2. Testing list_examples(tag='beginner')...
[Shows filtered results]

3. Testing get_example('basic')...
[Shows complete example with script and documentation]

4. Testing search_examples('Message')...
[Shows search results]

5. Testing analyze_script('basic')...
[Shows script analysis]

6. Testing compare_examples('basic', 'mpl-payload-log')...
[Shows comparison]

=== All tests completed successfully! ===
```

### Option 2: Interactive Python Testing

Test individual functions interactively:

```python
# Start Python in the project directory
python

# Import and test
import asyncio
from mcp_server import SAPGroovyMCPServer

async def test():
    server = SAPGroovyMCPServer()
    
    # Test listing examples
    result = await server.list_examples()
    print(result[0].text)
    
    # Test getting an example
    result = await server.get_example("basic")
    print(result[0].text)
    
    # Test search
    result = await server.search_examples("XML")
    print(result[0].text)

# Run the test
asyncio.run(test())
```

### Option 3: Test MCP Protocol Directly

Test the server's stdio communication:

```bash
# Start the server
python mcp_server.py
```

The server will wait for JSON-RPC messages on stdin. You can send MCP protocol messages manually or use an MCP client.

## Integration Testing with MCP Clients

### Testing with Claude Desktop

1. **Locate Claude Desktop config file:**
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

2. **Add the MCP server configuration:**
   ```json
   {
     "mcpServers": {
       "sap-groovy": {
         "command": "C:\\ProgramData\\miniforge3\\envs\\cpimcp\\python.exe",
         "args": ["c:\\Code\\sap\\cpi-groovy-examples.worktrees\\copilot-worktree-2026-01-13T12-40-20\\mcp_server.py"]
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Test with queries:**
   - "List all SAP CPI Groovy examples"
   - "Show me the basic example"
   - "Search for XML processing examples"
   - "Analyze the reading-credentials script"
   - "Compare basic and mpl-payload-log"

### Testing with MCP Inspector

Use the official MCP Inspector tool:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run the inspector
mcp-inspector python mcp_server.py
```

This opens a web UI where you can:
- View available resources
- Test all tools interactively
- See request/response logs
- Validate protocol compliance

## Verification Checklist

### ✅ Basic Functionality
- [ ] Server starts without errors
- [ ] Lists all 16+ Groovy examples
- [ ] Retrieves individual examples
- [ ] Search returns relevant results
- [ ] Script analysis extracts imports/functions
- [ ] Comparison shows differences

### ✅ Resources
- [ ] `list_resources()` returns all example resources
- [ ] `read_resource()` retrieves script content
- [ ] `read_resource()` retrieves README content
- [ ] `read_resource()` retrieves metadata

### ✅ Tools
- [ ] `list_examples` - Lists all examples
- [ ] `list_examples` with tag filter works
- [ ] `get_example` - Retrieves complete example
- [ ] `search_examples` - Finds matching examples
- [ ] `analyze_script` - Analyzes script structure
- [ ] `compare_examples` - Compares two examples

### ✅ Error Handling
- [ ] Invalid example name returns error
- [ ] Invalid resource URI returns error
- [ ] Missing files handled gracefully

### ✅ Performance
- [ ] Server starts in < 1 second
- [ ] Example discovery completes quickly
- [ ] No memory leaks during repeated calls

## Common Testing Issues

### Issue: "Module not found: mcp"

**Solution:**
```bash
pip install mcp pyyaml
```

### Issue: "Python not found"

**Solution:**
- Activate conda environment: `conda activate cpimcp`
- Or use full path: `C:\ProgramData\miniforge3\envs\cpimcp\python.exe`

### Issue: "No examples found"

**Solution:**
- Ensure you're in the correct directory
- Verify `script.groovy` files exist in subdirectories
- Check file permissions

### Issue: Claude Desktop doesn't show the server

**Solution:**
1. Check config file syntax (valid JSON)
2. Use absolute paths in configuration
3. Restart Claude Desktop completely
4. Check Claude logs for connection errors

## Advanced Testing

### Performance Testing

```python
import asyncio
import time
from mcp_server import SAPGroovyMCPServer

async def benchmark():
    server = SAPGroovyMCPServer()
    
    # Time listing examples
    start = time.time()
    await server.list_examples()
    print(f"List examples: {time.time() - start:.3f}s")
    
    # Time getting an example
    start = time.time()
    await server.get_example("basic")
    print(f"Get example: {time.time() - start:.3f}s")
    
    # Time search
    start = time.time()
    await server.search_examples("Message")
    print(f"Search: {time.time() - start:.3f}s")

asyncio.run(benchmark())
```

### Load Testing

```python
import asyncio
from mcp_server import SAPGroovyMCPServer

async def load_test():
    server = SAPGroovyMCPServer()
    
    # Run 100 concurrent requests
    tasks = []
    for i in range(100):
        tasks.append(server.list_examples())
    
    results = await asyncio.gather(*tasks)
    print(f"Completed 100 requests: {len(results)} responses")

asyncio.run(load_test())
```

### Protocol Compliance Testing

Test that responses conform to MCP specification:

```python
import asyncio
from mcp_server import SAPGroovyMCPServer

async def test_protocol():
    server = SAPGroovyMCPServer()
    
    # Test tool list
    tools = await server.server.list_tools()
    assert len(tools) == 5
    for tool in tools:
        assert tool.name
        assert tool.description
        assert tool.inputSchema
    
    print("✅ Protocol compliance verified")

asyncio.run(test_protocol())
```

## Continuous Testing

### Watch Mode

For development, you can set up auto-reload:

```bash
# Install watchdog
pip install watchdog

# Watch for changes and rerun tests
watchmedo shell-command --patterns="*.py" --recursive --command='python test_server.py'
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
cd "$(git rev-parse --show-toplevel)"
python test_server.py
if [ $? -ne 0 ]; then
    echo "Tests failed! Commit aborted."
    exit 1
fi
```

## Test Results Documentation

Document your test results:

```markdown
# Test Run: [Date]

## Environment
- Python: [version]
- MCP SDK: [version]
- OS: [Windows/macOS/Linux]

## Results
- ✅ All tools working
- ✅ Resources accessible
- ✅ Error handling correct
- ⚠️  Performance issue: [describe]
- ❌ Bug found: [describe]

## Notes
[Any observations or issues]
```

## Getting Help

If tests fail:

1. Check the IMPLEMENTATION_SUMMARY.md
2. Review MCP_SERVER_README.md troubleshooting section
3. Enable debug logging: Set `logging.basicConfig(level=logging.DEBUG)`
4. Check Python version: `python --version` (need 3.10+)
5. Verify dependencies: `pip list | grep -E "mcp|pyyaml"`

## Summary

✅ **Recommended Testing Flow:**
1. Run `python test_server.py` for quick validation
2. Test integration with Claude Desktop
3. Try example queries in production
4. Monitor for errors or issues

The test script validates all core functionality and is the fastest way to verify the MCP server is working correctly.
