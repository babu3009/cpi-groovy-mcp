# SAP Groovy MCP Server

A Model Context Protocol (MCP) server that provides intelligent access to SAP Cloud Integration (CPI) Groovy script examples.

## Credits / Attribution

- Groovy examples and repository structure are based on Fatih Pense's work: https://github.com/pizug/cpi-groovy-examples
- The MCP server implementation is created by babu3009: https://github.com/babu3009/cpi-groovy-mcp
- Workspace/contact: https://www.linkedin.com/in/isaiyavan/

## Overview

This MCP server enables AI assistants to explore, analyze, and understand SAP CPI Groovy script examples.

## Server options in this workspace

### Option A: Quick server (single file)

- Location: `cpi-groovy-examples/mcp_server.py`
- Good for: quick local testing and simple browsing

**Tools:** `list_examples`, `get_example`, `search_examples`, `analyze_script`, `compare_examples`

### Option B: Plan-aligned server (manifest/registry + pytest)

- Location: `sap-groovy-mcp/`
- Good for: deterministic corpus consumption + tests
- Aligns with: `.github/prompts/plan-sapGroovyMcp.prompt.md`

## Install (Option A)

From `cpi-groovy-examples/`:

```bash
pip install -r requirements.txt
```

## Configure an MCP client (Option A)

Example for Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "sap-groovy": {
      "command": "python",
      "args": ["C:\\Code\\sap\\cpi-groovy-examples\\mcp_server.py"]
    }
  }
}
```

## Unit-style validation (Option A)

From `cpi-groovy-examples/`:

```bash
python test_server.py
```

