# QR Code Generator MCP Server

An MCP (Model Context Protocol) server that generates QR codes from URLs for integration with Q CLI and cao supervisor workflows.

## Features

- Generates QR codes from any URL
- Returns base64-encoded PNG images
- Configurable QR code size and border
- Seamless integration with Q CLI agents
- Automatic process management via Q CLI

## Prerequisites

- Linux/WSL environment
- Python 3.12+
- Q CLI installed and configured
- cao supervisor workflow setup

## Installation & Setup

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3-pip python3.12-venv build-essential
```

### 2. Setup Virtual Environment

```bash
# Navigate to the qrcode_mcp_server directory
cd qrcode_mcp_server

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Test Installation

```bash
# Test the QR code generation
python test_mcp.py

# Should output:
# ✓ URL: https://wikipedia.org
# ✓ Base64 length: 764 characters
# ✓ QR code saved to 'test_qr_mcp.png'
# ✓ Test completed successfully!
```

### 4. Configure Q CLI Agent

Add to your supervisor agent configuration (`supervisor.md`):

```yaml
mcpServers:
  qrcode-mcp-server:
    type: stdio
    command: /absolute/path/to/qrcode_mcp_server/venv/bin/python
    args:
      - "/absolute/path/to/qrcode_mcp_server/server.py"

allowedTools: ["@qrcode-mcp-server", "other-tools..."]
```

**Important**: Replace `/absolute/path/to/` with your actual workspace path.




### Available Tool

**`@qrcode-mcp-server/generate_qr_code`**

Parameters:
- `url` (required): The URL to encode in the QR code
- `size` (optional): Box size for QR code, default is 10
- `border` (optional): Border size in boxes, default is 4

### Example Usage in Agent

```python
# Agent can call:
generate_qr_code(
    url="https://github.com/your-repo",
    size=10,
    border=4
)
```

## Integration with cao Supervisor

The QR Code MCP Server integrates as the first step in the cao supervisor workflow:

1. **Project Initialization & QR Code Generation**
   - Creates project directory
   - Generates QR code for GitHub repository
   - Saves QR code as PNG file


## File Structure

```
qrcode_mcp_server/
├── server.py              # Main MCP server
├── test_mcp.py            # Test script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── venv/                 # Virtual environment
└── qr-code/test_qr_mcp.png      # Test output (generated)
```

## Output Files

When used in projects, generates:
- `qr-code.png` - QR code image file

## Troubleshooting

### Permission Issues
```bash
chmod +x server.py
```

### Path Issues
- Always use absolute paths in agent configurations
- Verify virtual environment path exists

### Dependencies Check
```bash
source venv/bin/activate
pip list | grep -E "(mcp|qrcode|Pillow)"
```

### Test MCP Server Directly
```bash
source venv/bin/activate
python server.py
# Should start without errors
```

## Technical Details

- **Protocol**: Model Context Protocol (MCP) v2024-11-05
- **Communication**: stdin/stdout JSON-RPC
- **Image Format**: PNG with base64 encoding
- **QR Code Library**: qrcode[pil] with Pillow
- **Error Correction**: Level L (Low)

## Dependencies

- `mcp>=1.0.0` - Model Context Protocol framework
- `qrcode[pil]>=7.4.2` - QR code generation with PIL support
- `Pillow>=10.4.0` - Image processing library

## License

Part of the echo-architect-orchestrator project.
