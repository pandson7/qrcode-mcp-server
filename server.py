#!/usr/bin/env python3
"""
QR Code Generator MCP Server

An MCP server that generates QR codes from URLs and returns them as base64-encoded PNG images.
"""

import base64
from io import BytesIO
import qrcode
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio


# Create server instance
app = Server("qr-code-generator")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="generate_qr_code",
            description="Generate a QR code from a URL and return it as a base64-encoded PNG image",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to encode in the QR code"
                    },
                    "size": {
                        "type": "integer",
                        "description": "Box size for QR code (default: 10)",
                        "default": 10
                    },
                    "border": {
                        "type": "integer",
                        "description": "Border size in boxes (default: 4)",
                        "default": 4
                    }
                },
                "required": ["url"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls."""
    if name != "generate_qr_code":
        raise ValueError(f"Unknown tool: {name}")
    
    url = arguments.get("url")
    if not url:
        raise ValueError("URL is required")
    
    size = arguments.get("size", 10)
    border = arguments.get("border", 4)
    
    try:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return [
            TextContent(
                type="text",
                text=f"QR code generated successfully for: {url}\n\nBase64 PNG Image:\n{img_base64}\n\nTo view, save this as a .png file or use in HTML: <img src=\"data:image/png;base64,{img_base64}\" />"
            )
        ]
    
    except Exception as e:
        raise RuntimeError(f"Failed to generate QR code: {str(e)}")


async def main():
    """Run the MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
