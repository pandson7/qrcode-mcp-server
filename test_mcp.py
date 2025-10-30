"""
Test script for the QR Code MCP server
Tests the QR code generation logic directly
"""
import base64
from io import BytesIO
import qrcode


def generate_qr_code(url: str, size: int = 10, border: int = 4) -> str:
    """Generate QR code and return base64 string"""
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
    
    return img_base64


def test_generate_qr():
    """Test QR code generation"""
    print("Testing QR code generation for Wikipedia...")
    
    url = "https://wikipedia.org"
    base64_img = generate_qr_code(url, size=10, border=4)
    
    print(f"✓ URL: {url}")
    print(f"✓ Base64 length: {len(base64_img)} characters")
    
    # Save to file
    img_data = base64.b64decode(base64_img)
    with open('test_qr_mcp.png', 'wb') as f:
        f.write(img_data)
    
    print(f"✓ QR code saved to 'test_qr_mcp.png'")
    print(f"✓ File size: {len(img_data)} bytes")
    print(f"\n✓ Test completed successfully!")
    print(f"\nThe MCP server will use this same logic when called.")


if __name__ == "__main__":
    test_generate_qr()
