
import os
import fitz
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")

os.makedirs(INVOICE_DIR, exist_ok=True)

# Create a scanned-looking invoice image
image = Image.new("RGB", (1200, 1600), "white")
draw = ImageDraw.Draw(image)

font_path = r"C:\Windows\Fonts\arial.ttf"
font = ImageFont.truetype(font_path, 42)
heading_font = ImageFont.truetype(font_path, 65)

draw.text((400, 120), "INVOICE", fill="black", font=heading_font)

invoice_details = [
    "Invoice Number: OCR-2026-001",
    "Vendor: ABC Technologies",
    "Date: 2026-11-20",
    "Currency: INR",
    "Subtotal: Rs. 42857.14",
    "Tax: Rs. 2142.86",
    "Total: Rs. 45000",
    "Amount: Rs. 45000",
    "Thank you for your business!"
]

y = 350

for line in invoice_details:
    draw.text((120, y), line, fill="black", font=font)
    y += 120

# Save image
image_path = os.path.join(INVOICE_DIR, "scanned_sample.png")
image.save(image_path)

# Convert image into an image-only PDF
pdf_path = os.path.join(INVOICE_DIR, "scanned_sample.pdf")

doc = fitz.open()
page = doc.new_page(width=600, height=800)

page.insert_image(
    page.rect,
    filename=image_path
)

doc.save(pdf_path)
doc.close()

print("Scanned sample invoice created successfully!")
print("PDF:", pdf_path)
