#!/usr/bin/env python3
"""
SAP Cloud Integration Groovy Examples MCP Server

This MCP server provides tools to explore and understand SAP CPI Groovy script examples.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Any, Optional
import yaml

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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sap-groovy-mcp")

# Base directory for examples
BASE_DIR = Path(__file__).parent

class SAPGroovyMCPServer:
    def __init__(self):
        self.server = Server("sap-groovy-mcp")
        self.setup_handlers()
        
    def setup_handlers(self):
        @self.server.list_resources()
        async def handle_list_resources() -> list[Resource]:
            """List all available Groovy example resources."""
            resources = []
            
            # Scan all directories for script.groovy files
            for groovy_file in BASE_DIR.glob("**/script.groovy"):
                example_dir = groovy_file.parent
                example_name = example_dir.name
                
                # Add script resource
                resources.append(
                    Resource(
                        uri=f"groovy://examples/{example_name}/script",
                        name=f"{example_name} - Script",
                        description=f"Groovy script for {example_name}",
                        mimeType="text/x-groovy"
                    )
                )
                
                # Add README if exists
                readme_path = example_dir / "README.md"
                if readme_path.exists():
                    resources.append(
                        Resource(
                            uri=f"groovy://examples/{example_name}/readme",
                            name=f"{example_name} - Documentation",
                            description=f"Documentation for {example_name}",
                            mimeType="text/markdown"
                        )
                    )
                
                # Add metadata if exists
                meta_path = example_dir / "meta.yaml"
                if meta_path.exists():
                    resources.append(
                        Resource(
                            uri=f"groovy://examples/{example_name}/meta",
                            name=f"{example_name} - Metadata",
                            description=f"Metadata for {example_name}",
                            mimeType="application/yaml"
                        )
                    )
            
            return resources
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """Read a specific Groovy example resource."""
            if not uri.startswith("groovy://examples/"):
                raise ValueError(f"Unknown resource: {uri}")
            
            # Parse URI: groovy://examples/{example_name}/{type}
            parts = uri.replace("groovy://examples/", "").split("/")
            if len(parts) != 2:
                raise ValueError(f"Invalid resource URI: {uri}")
            
            example_name, resource_type = parts
            example_dir = BASE_DIR / example_name
            
            if not example_dir.exists():
                raise ValueError(f"Example not found: {example_name}")
            
            if resource_type == "script":
                file_path = example_dir / "script.groovy"
            elif resource_type == "readme":
                file_path = example_dir / "README.md"
            elif resource_type == "meta":
                file_path = example_dir / "meta.yaml"
            else:
                raise ValueError(f"Unknown resource type: {resource_type}")
            
            if not file_path.exists():
                raise ValueError(f"Resource file not found: {file_path}")
            
            return file_path.read_text(encoding="utf-8")
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[Tool]:
            """List available tools."""
            return [
                Tool(
                    name="list_examples",
                    description="List all available SAP CPI Groovy script examples with their metadata",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "tag": {
                                "type": "string",
                                "description": "Filter examples by tag (e.g., 'beginner', 'xml', 'csv')"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_example",
                    description="Get detailed information about a specific Groovy example including script, documentation, and metadata",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "example_name": {
                                "type": "string",
                                "description": "Name of the example (e.g., 'basic', 'mpl-payload-log')"
                            }
                        },
                        "required": ["example_name"]
                    }
                ),
                Tool(
                    name="search_examples",
                    description="Search for examples by keyword in documentation and scripts",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="analyze_script",
                    description="Analyze a Groovy script to extract imports, functions, and key concepts",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "example_name": {
                                "type": "string",
                                "description": "Name of the example to analyze"
                            }
                        },
                        "required": ["example_name"]
                    }
                ),
                Tool(
                    name="compare_examples",
                    description="Compare two examples to understand differences and similarities",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "example1": {
                                "type": "string",
                                "description": "First example name"
                            },
                            "example2": {
                                "type": "string",
                                "description": "Second example name"
                            }
                        },
                        "required": ["example1", "example2"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool execution."""
            
            if name == "list_examples":
                return await self.list_examples(arguments.get("tag"))
            elif name == "get_example":
                return await self.get_example(arguments["example_name"])
            elif name == "search_examples":
                return await self.search_examples(arguments["query"])
            elif name == "analyze_script":
                return await self.analyze_script(arguments["example_name"])
            elif name == "compare_examples":
                return await self.compare_examples(arguments["example1"], arguments["example2"])
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def list_examples(self, tag: Optional[str] = None) -> list[TextContent]:
        """List all examples with their metadata."""
        examples = []
        
        for example_dir in sorted(BASE_DIR.iterdir()):
            if not example_dir.is_dir() or example_dir.name.startswith("."):
                continue
            
            script_path = example_dir / "script.groovy"
            if not script_path.exists():
                # Check for other groovy files
                groovy_files = list(example_dir.glob("*.groovy"))
                if not groovy_files:
                    continue
            
            # Read metadata if available
            meta_path = example_dir / "meta.yaml"
            metadata = {}
            if meta_path.exists():
                try:
                    metadata = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
                except Exception as e:
                    logger.warning(f"Failed to parse metadata for {example_dir.name}: {e}")
            
            # Filter by tag if specified
            if tag:
                tags = metadata.get("tags", [])
                if tag not in tags:
                    continue
            
            # Get first line of README as description
            readme_path = example_dir / "README.md"
            description = ""
            if readme_path.exists():
                try:
                    first_line = readme_path.read_text(encoding="utf-8").split("\n")[0]
                    description = first_line.lstrip("# ").strip()
                except Exception:
                    pass
            
            examples.append({
                "name": example_dir.name,
                "description": description,
                "author": metadata.get("author", "Unknown"),
                "tags": metadata.get("tags", [])
            })
        
        result = "# SAP CPI Groovy Examples\n\n"
        if tag:
            result += f"Filtered by tag: **{tag}**\n\n"
        
        for ex in examples:
            result += f"## {ex['name']}\n"
            if ex['description']:
                result += f"{ex['description']}\n"
            result += f"- **Author:** {ex['author']}\n"
            if ex['tags']:
                result += f"- **Tags:** {', '.join(ex['tags'])}\n"
            result += "\n"
        
        return [TextContent(type="text", text=result)]
    
    async def get_example(self, example_name: str) -> list[TextContent]:
        """Get detailed information about an example."""
        example_dir = BASE_DIR / example_name
        
        if not example_dir.exists() or not example_dir.is_dir():
            raise ValueError(f"Example not found: {example_name}")
        
        result = f"# {example_name}\n\n"
        
        # Read README
        readme_path = example_dir / "README.md"
        if readme_path.exists():
            result += "## Documentation\n\n"
            result += readme_path.read_text(encoding="utf-8") + "\n\n"
        
        # Read metadata
        meta_path = example_dir / "meta.yaml"
        if meta_path.exists():
            try:
                metadata = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
                result += "## Metadata\n\n"
                result += f"```yaml\n{yaml.dump(metadata, default_flow_style=False)}```\n\n"
            except Exception as e:
                logger.warning(f"Failed to parse metadata: {e}")
        
        # Read script
        script_path = example_dir / "script.groovy"
        if script_path.exists():
            result += "## Groovy Script\n\n"
            result += f"```groovy\n{script_path.read_text(encoding='utf-8')}\n```\n\n"
        else:
            # Find any groovy file
            groovy_files = list(example_dir.glob("*.groovy"))
            if groovy_files:
                for gf in groovy_files:
                    result += f"## Groovy Script: {gf.name}\n\n"
                    result += f"```groovy\n{gf.read_text(encoding='utf-8')}\n```\n\n"
        
        # List input/output files
        result += "## Files\n\n"
        for file in sorted(example_dir.iterdir()):
            if file.is_file() and file.suffix not in [".groovy", ".md", ".yaml"]:
                result += f"- `{file.name}`\n"
        
        return [TextContent(type="text", text=result)]
    
    async def search_examples(self, query: str) -> list[TextContent]:
        """Search for examples by keyword."""
        query_lower = query.lower()
        results = []
        
        for example_dir in sorted(BASE_DIR.iterdir()):
            if not example_dir.is_dir() or example_dir.name.startswith("."):
                continue
            
            matches = []
            
            # Search in README
            readme_path = example_dir / "README.md"
            if readme_path.exists():
                try:
                    content = readme_path.read_text(encoding="utf-8")
                    if query_lower in content.lower():
                        matches.append("README")
                except Exception:
                    pass
            
            # Search in script
            for groovy_file in example_dir.glob("*.groovy"):
                try:
                    content = groovy_file.read_text(encoding="utf-8")
                    if query_lower in content.lower():
                        matches.append(f"Script: {groovy_file.name}")
                except Exception:
                    pass
            
            if matches:
                results.append({
                    "name": example_dir.name,
                    "matches": matches
                })
        
        if not results:
            return [TextContent(type="text", text=f"No examples found matching '{query}'")]
        
        result = f"# Search Results for '{query}'\n\n"
        result += f"Found {len(results)} example(s):\n\n"
        
        for res in results:
            result += f"## {res['name']}\n"
            result += f"Matches in: {', '.join(res['matches'])}\n\n"
        
        return [TextContent(type="text", text=result)]
    
    async def analyze_script(self, example_name: str) -> list[TextContent]:
        """Analyze a Groovy script."""
        example_dir = BASE_DIR / example_name
        
        if not example_dir.exists():
            raise ValueError(f"Example not found: {example_name}")
        
        # Find groovy file
        script_path = example_dir / "script.groovy"
        if not script_path.exists():
            groovy_files = list(example_dir.glob("*.groovy"))
            if not groovy_files:
                raise ValueError(f"No Groovy script found in {example_name}")
            script_path = groovy_files[0]
        
        content = script_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        # Extract imports
        imports = [line.strip() for line in lines if line.strip().startswith("import ")]
        
        # Extract functions
        functions = []
        for i, line in enumerate(lines):
            if "def " in line and "(" in line:
                functions.append(line.strip())
        
        # Extract key SAP CPI concepts
        concepts = []
        if "Message" in content:
            concepts.append("Message manipulation")
        if "getBody" in content or "setBody" in content:
            concepts.append("Body processing")
        if "getHeader" in content or "setHeader" in content:
            concepts.append("Header manipulation")
        if "getProperty" in content or "setProperty" in content:
            concepts.append("Property manipulation")
        if "messageLog" in content:
            concepts.append("Message logging")
        if "SecureStoreService" in content:
            concepts.append("Credential management")
        if "xml" in content.lower():
            concepts.append("XML processing")
        if "csv" in content.lower():
            concepts.append("CSV processing")
        
        result = f"# Script Analysis: {example_name}\n\n"
        
        result += "## Imports\n\n"
        if imports:
            for imp in imports:
                result += f"- `{imp}`\n"
        else:
            result += "No imports found.\n"
        result += "\n"
        
        result += "## Functions\n\n"
        if functions:
            for func in functions:
                result += f"- `{func}`\n"
        else:
            result += "No functions found.\n"
        result += "\n"
        
        result += "## Key Concepts\n\n"
        if concepts:
            for concept in concepts:
                result += f"- {concept}\n"
        else:
            result += "No specific concepts identified.\n"
        result += "\n"
        
        result += f"## Statistics\n\n"
        result += f"- Lines of code: {len(lines)}\n"
        result += f"- Import statements: {len(imports)}\n"
        result += f"- Functions: {len(functions)}\n"
        
        return [TextContent(type="text", text=result)]
    
    async def compare_examples(self, example1: str, example2: str) -> list[TextContent]:
        """Compare two examples."""
        result = f"# Comparing Examples: {example1} vs {example2}\n\n"
        
        # Get both examples
        ex1_dir = BASE_DIR / example1
        ex2_dir = BASE_DIR / example2
        
        if not ex1_dir.exists():
            raise ValueError(f"Example not found: {example1}")
        if not ex2_dir.exists():
            raise ValueError(f"Example not found: {example2}")
        
        # Compare file structures
        ex1_files = set(f.name for f in ex1_dir.iterdir() if f.is_file())
        ex2_files = set(f.name for f in ex2_dir.iterdir() if f.is_file())
        
        result += "## File Structure\n\n"
        result += f"### Common files\n"
        common = ex1_files & ex2_files
        for f in sorted(common):
            result += f"- {f}\n"
        result += "\n"
        
        result += f"### Only in {example1}\n"
        only_ex1 = ex1_files - ex2_files
        if only_ex1:
            for f in sorted(only_ex1):
                result += f"- {f}\n"
        else:
            result += "None\n"
        result += "\n"
        
        result += f"### Only in {example2}\n"
        only_ex2 = ex2_files - ex1_files
        if only_ex2:
            for f in sorted(only_ex2):
                result += f"- {f}\n"
        else:
            result += "None\n"
        result += "\n"
        
        # Compare scripts
        script1_path = ex1_dir / "script.groovy"
        script2_path = ex2_dir / "script.groovy"
        
        if script1_path.exists() and script2_path.exists():
            content1 = script1_path.read_text(encoding="utf-8")
            content2 = script2_path.read_text(encoding="utf-8")
            
            # Extract imports for comparison
            imports1 = set(line.strip() for line in content1.split("\n") if line.strip().startswith("import "))
            imports2 = set(line.strip() for line in content2.split("\n") if line.strip().startswith("import "))
            
            result += "## Imports Comparison\n\n"
            result += f"### Common imports\n"
            common_imports = imports1 & imports2
            if common_imports:
                for imp in sorted(common_imports):
                    result += f"- `{imp}`\n"
            else:
                result += "None\n"
            result += "\n"
            
            result += f"### Only in {example1}\n"
            only_imports1 = imports1 - imports2
            if only_imports1:
                for imp in sorted(only_imports1):
                    result += f"- `{imp}`\n"
            else:
                result += "None\n"
            result += "\n"
            
            result += f"### Only in {example2}\n"
            only_imports2 = imports2 - imports1
            if only_imports2:
                for imp in sorted(only_imports2):
                    result += f"- `{imp}`\n"
            else:
                result += "None\n"
        
        return [TextContent(type="text", text=result)]
    
    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="sap-groovy-mcp",
                    server_version="0.1.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

async def main():
    """Main entry point."""
    server = SAPGroovyMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
