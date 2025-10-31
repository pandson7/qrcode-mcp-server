#!/usr/bin/env python3
"""
QR Code Generator MCP Server

An MCP server that generates QR codes from URLs and returns them as base64-encoded PNG images.
Built with FastMCP for simplicity.
"""

import base64
from io import BytesIO
import qrcode
from fastmcp import FastMCP

# Create FastMCP server
mcp = FastMCP("qr_code_generator")


@mcp.tool()
def generate_qr_code(url: str, size: int = 10, border: int = 4) -> str:
    """
    Generate a QR code from a URL and return it as a base64-encoded PNG image.
    
    Args:
        url: The URL to encode in the QR code
        size: Box size for QR code (default: 10)
        border: Border size in boxes (default: 4)
    
    Returns:
        Base64-encoded PNG image of the QR code
    """
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
    
    return f"QR code generated successfully for: {url}\n\nBase64 PNG Image:\n{img_base64}\n\nTo view, save this as a .png file or use in HTML: <img src=\"data:image/png;base64,{img_base64}\" />"


if __name__ == "__main__":
    mcp.run()
