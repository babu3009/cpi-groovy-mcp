# Groovy Script Examples for SAP Cloud Integration now known as SAP Integration Suite

Groovy scripting is an integral and important feature of SAP Cloud Integration (CPI), now known as SAP Integration Suite (SAP IS).

The goals of this repository are:

- Providing reusable Groovy script templates for SAP Cloud Integration (CPI) / SAP Integration Suite (SAP IS)
- Making common integration tasks easy to find (headers/properties, transformations, logging, error handling, connectivity)
- Including runnable-style fixtures (input/expected files) where applicable to speed up testing and validation
- Enabling fast discovery via documentation + MCP tooling (browse, search, analyze, compare examples)

Script examples are provided with context, explanation, and input/output examples.

You can see the examples in a more visual format on [pizug.com/cpi-groovy-examples](https://pizug.com/cpi-groovy-examples) (base code author Fatih Pense)

# MCP Server (AI tooling)

This workspace also includes an MCP server for browsing/searching these examples.

- Base Groovy examples/repo: https://github.com/pizug/cpi-groovy-examples (Fatih Pense)
- MCP implementation: https://github.com/babu3009/cpi-groovy-mcp (babu3009)
- Workspace/contact: https://www.linkedin.com/in/isaiyavan/

## Implementation details

This workspace contains two ways to expose these examples via MCP:

1. Quick server (single file)

- Entry point: `mcp_server.py`
- Tools: list examples, retrieve an example, search, analyze a script, compare two examples
- Validation: `python test_server.py`

2. Plan-aligned server (manifest/registry + pytest)

- A separate Python package under `c:\Code\sap\sap-groovy-mcp\` (sibling folder in this workspace)
- Generates deterministic corpus artifacts (`registry.json`, `manifest.json`) and validates them with pytest

See MCP_SERVER_README.md for setup and configuration examples.

## Documentation

- [MCP_SERVER_README.md](MCP_SERVER_README.md): MCP server overview, install steps, and MCP client configuration examples.
- [TESTING_GUIDE.md](TESTING_GUIDE.md): how to validate the server(s), plus common troubleshooting tips.
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md): short summary of what’s implemented in this workspace.

# How to contribute

You can send any kind of example that you consider to be useful. We can analyze it together, add it to an existing script, or create a new one.

You can [create a new issue](https://github.com/babu3009/cpi-groovy-mcp/issues/new) or send it directly to [me](https://www.linkedin.com/in/isaiyavan/).

If you can create good documentation for scripts, that is great. If you don't have the time, don't worry, we will improve it together over time.

# License

- Imported SAP Java APIs for CPI are property of SAP.
- Community provided Groovy scripts are MIT licenced.
- Script explanations, `README.md` files are licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
