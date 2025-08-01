from PIL import Image
from pathlib import Path
import struct

# ICNS icon types mapped by size in pixels
ICNS_TYPES = {
    16: 'icp4',
    32: 'icp5',
    64: 'icp6',
    128: 'ic07',
    256: 'ic08',
    512: 'ic09',
    1024: 'ic10',
}

def write_icns_header(f, length):
    f.write(b'icns')
    f.write(struct.pack(">I", length))

def write_icns_icon(f, icon_type, data):
    f.write(icon_type.encode('ascii'))
    f.write(struct.pack(">I", len(data) + 8))
    f.write(data)

def convert_to_icns(input_path, output_path="icon.icns", size=None):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if input_path.suffix.lower() not in [".png", ".jpg", ".jpeg"]:
        raise ValueError("Only PNG, JPG, and JPEG formats are supported.")

    img = Image.open(input_path).convert("RGBA")

    # Use provided size or original image size
    if size is None:
        size = img.width
        if img.width != img.height:
            raise ValueError("Input image must be square or specify size explicitly.")
    else:
        img = img.resize((size, size), Image.LANCZOS)

    if size not in ICNS_TYPES:
        raise ValueError(f"Unsupported icon size {size}px. Supported sizes: {list(ICNS_TYPES.keys())}")

    icon_type = ICNS_TYPES[size]

    from io import BytesIO
    png_bytes_io = BytesIO()
    img.save(png_bytes_io, format="PNG")
    png_bytes = png_bytes_io.getvalue()

    total_length = 8 + 8 + len(png_bytes)  # icns header + chunk header + png data

    with open(output_path, "wb") as f:
        write_icns_header(f, total_length)
        write_icns_icon(f, icon_type, png_bytes)

    return output_path
