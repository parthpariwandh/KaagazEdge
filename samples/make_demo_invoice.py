from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    dest = Path(__file__).parent / "demo_invoice.png"
    img = Image.new("RGB", (1240, 1754), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1240, 140), fill=(10, 18, 36))
    draw.rectangle((0, 0, 28, 1754), fill=(196, 30, 58))
    font = ImageFont.load_default()
    draw.text((60, 50), "SAMPLE TRADERS KOLKATA    TAX INVOICE", fill=(255, 255, 255), font=font)
    lines = [
        "GSTIN 19AAAAA0000A1Z5",
        "Invoice INV-2026-0142    Date 01 Sep 2026",
        "Buyer: Riverside Workshop",
        "Place of supply: West Bengal",
        "Grand total INR 11800",
        "Demo page for KaagazEdge. Not a real tax document.",
    ]
    y = 180
    for line in lines:
        draw.text((60, y), line, fill=(22, 24, 29), font=font)
        y += 36
    img.save(dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()
