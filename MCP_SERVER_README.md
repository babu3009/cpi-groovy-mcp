# SAP Groovy MCP Server

A Model Context Protocol (MCP) server that provides intelligent access to SAP Cloud Integration (CPI) Groovy script examples.

## Overview

This MCP server enables AI assistants to explore, analyze, and understand SAP CPI Groovy script examples. It provides structured access to a collection of real-world integration scripts with documentation, metadata, and analysis capabilities.

## Features

### Resources
<<<<<<< Updated upstream

The server exposes Groovy examples as resources with three components:

=======
<<<<<<< Updated upstream
The server exposes Groovy examples as resources with three components:
=======

The server exposes Groovy examples as resources with three components:

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- **Script** (`groovy://examples/{name}/script`) - The Groovy script file
- **Documentation** (`groovy://examples/{name}/readme`) - README with explanations
- **Metadata** (`groovy://examples/{name}/meta`) - YAML metadata with author and tags

### Tools

#### 1. `list_examples`
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
Lists all available SAP CPI Groovy examples with metadata.

**Parameters:**
- `tag` (optional): Filter examples by tag (e.g., "beginner", "xml", "csv")

**Example:**
=======
>>>>>>> Stashed changes

Lists all available SAP CPI Groovy examples with metadata.

**Parameters:**

- `tag` (optional): Filter examples by tag (e.g., "beginner", "xml", "csv")

**Example:**

<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
```json
{
  "tag": "beginner"
}
```

#### 2. `get_example`
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
Retrieves detailed information about a specific example including script, documentation, and all related files.

**Parameters:**
- `example_name` (required): Name of the example directory

**Example:**
=======
>>>>>>> Stashed changes

Retrieves detailed information about a specific example including script, documentation, and all related files.

**Parameters:**

- `example_name` (required): Name of the example directory

**Example:**

<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
```json
{
  "example_name": "basic"
}
```

#### 3. `search_examples`
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
Searches for examples by keyword in documentation and scripts.

**Parameters:**
- `query` (required): Search query string

**Example:**
=======
>>>>>>> Stashed changes

Searches for examples by keyword in documentation and scripts.

**Parameters:**

- `query` (required): Search query string

**Example:**

<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
```json
{
  "query": "XML processing"
}
```

#### 4. `analyze_script`
<<<<<<< Updated upstream

Analyzes a Groovy script to extract:

=======
<<<<<<< Updated upstream
Analyzes a Groovy script to extract:
=======

Analyzes a Groovy script to extract:

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- Import statements
- Function definitions
- Key SAP CPI concepts (Message, Headers, Properties, etc.)
- Code statistics

**Parameters:**
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
- `example_name` (required): Name of the example to analyze

**Example:**
=======
>>>>>>> Stashed changes

- `example_name` (required): Name of the example to analyze

**Example:**

<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
```json
{
  "example_name": "mpl-payload-log"
}
```

#### 5. `compare_examples`
<<<<<<< Updated upstream

Compares two examples to identify:

=======
<<<<<<< Updated upstream
Compares two examples to identify:
=======

Compares two examples to identify:

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- Common and unique files
- Shared and different imports
- Structural differences

**Parameters:**
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- `example1` (required): First example name
- `example2` (required): Second example name

**Example:**
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
```json
{
  "example1": "basic",
  "example2": "mpl-payload-log"
}
```

## Installation

### Prerequisites
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- Python 3.10 or higher
- pip package manager

### Steps

1. Install dependencies:
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
```bash
pip install -r requirements.txt
```

2. Configure your MCP client to use this server. Add to your MCP settings file:

**For Claude Desktop** (`claude_desktop_config.json`):
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
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

**For other MCP clients**, configure according to their documentation, using:
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- **Command**: `python` (or `python3`)
- **Args**: `["/path/to/mcp_server.py"]`

3. Restart your MCP client

## Usage Examples

### Listing Examples
<<<<<<< Updated upstream
=======
<<<<<<< Updated upstream
Ask your AI assistant:
> "List all beginner-friendly SAP CPI Groovy examples"

### Getting an Example
> "Show me the 'basic' example with full documentation"

### Searching
> "Find examples that work with XML"

### Analysis
> "Analyze the script in the 'reading-credentials' example"

### Comparison
=======
>>>>>>> Stashed changes

Ask your AI assistant:

> "List all beginner-friendly SAP CPI Groovy examples"

### Getting an Example

> "Show me the 'basic' example with full documentation"

### Searching

> "Find examples that work with XML"

### Analysis

> "Analyze the script in the 'reading-credentials' example"

### Comparison

<<<<<<< Updated upstream
=======
>>>>>>> Stashed changes
>>>>>>> Stashed changes
> "Compare the 'merge-two-xml' and 'merge-two-xml-v2' examples"

## Project Structure

```
cpi-groovy-examples/
├── mcp_server.py          # Main MCP server implementation
├── requirements.txt        # Python dependencies
├── package.json           # Project metadata
├── MCP_SERVER_README.md   # This file
└── [example directories]  # Individual Groovy examples
    ├── script.groovy      # Main script
    ├── README.md          # Documentation
    ├── meta.yaml          # Metadata (author, tags)
    └── [test files]       # Input/output test files
```

## Example Categories

Available examples cover:
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- **Basics**: Message manipulation, headers, properties
- **Data Transformation**: CSV to XML, XML to CSV, Excel processing
- **Logging**: MPL payload logs, custom headers
- **Integration**: SFTP operations, credential management
- **Error Handling**: HTTP and SOAP error handling
- **Advanced**: Large data handling, external JAR libraries

## Development

### Adding New Examples

To add a new example that the MCP server can discover:

1. Create a directory under the repository root
2. Add a `script.groovy` file
3. Add a `README.md` with documentation
4. Optionally add `meta.yaml` with:
   ```yaml
   author: Your Name
   tags:
     - category1
     - category2
   ```

The MCP server will automatically discover and expose the new example.

### Testing

Run the server directly:
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
```bash
python mcp_server.py
```

The server uses stdio for communication and follows the MCP protocol specification.

## Troubleshooting

### Server Not Starting
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- Ensure Python 3.10+ is installed: `python --version`
- Verify dependencies are installed: `pip install -r requirements.txt`
- Check that the path in your MCP client config is correct

### Examples Not Appearing
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- Verify the repository structure is intact
- Ensure `script.groovy` files exist in example directories
- Check file permissions

### Connection Issues
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- Restart your MCP client after configuration changes
- Check client logs for connection errors
- Verify the server command and arguments are correct

## Contributing

Contributions are welcome! Please refer to the main [README.md](README.md) for contribution guidelines.

## License

- MCP Server implementation: MIT License
- SAP CPI Groovy examples: MIT License
- Documentation: Creative Commons Attribution 4.0 International (CC BY 4.0)
- SAP Java APIs: Property of SAP

## Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [SAP Cloud Integration](https://help.sap.com/docs/cloud-integration)
- [Original Repository](https://github.com/pizug/cpi-groovy-examples)
- [Visual Examples](https://pizug.com/cpi-groovy-examples)

## Support

For issues or questions:
<<<<<<< Updated upstream

=======
<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
>>>>>>> Stashed changes
- Create an issue on GitHub
- Contact through [Groovy IDE](https://groovyide.com/cpi) feedback
- Connect with [Fatih Pense on LinkedIn](https://www.linkedin.com/in/fatihpense/)
