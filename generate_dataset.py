
import os
import random
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta

# Folder paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")

os.makedirs(INVOICE_DIR, exist_ok=True)

# Sample vendors
vendors = [
    "ABC Technologies",
    "Global Solutions",
    "Smart Enterprises",
    "Digital Services",
    "Tech World"
]

data = []

# Generate 20 invoices
for i in range(1, 21):

    invoice_no = f"INV-{1000 + i}"
    vendor = random.choice(vendors)

    amount = random.randint(1000, 50000)

    invoice_date = datetime.today() - timedelta(
        days=random.randint(1, 180)
    )

    anomaly = "No"

    # Generate unusual invoices
    if i in [5, 10, 15]:
        amount = random.randint(100000, 200000)
        anomaly = "Yes"

    # Generate duplicate invoices
    if i in [5, 7, 12]:
        invoice_no = "INV-1005"
        vendor = "Smart Enterprises"
        anomaly = "Yes"

    # Calculate subtotal and tax
    total = float(amount)
    subtotal = round(total / 1.18, 2)
    tax = round(total - subtotal, 2)

    currency = "INR"

    data.append({
        "File_Name": f"invoice_{i}.pdf",
        "Invoice_No": invoice_no,
        "Vendor": vendor,
        "Date": invoice_date.strftime("%Y-%m-%d"),
        "Currency": currency,
        "Subtotal": subtotal,
        "Tax": tax,
        "Total": total,
        "Amount": total,
        "Anomaly": anomaly
    })

    # Create PDF invoice
    pdf_path = os.path.join(
        INVOICE_DIR,
        f"invoice_{i}.pdf"
    )

    pdf = canvas.Canvas(pdf_path, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(180, 780, "INVOICE")

    pdf.setFont("Helvetica", 12)

    pdf.drawString(50, 730, f"Invoice Number: {invoice_no}")
    pdf.drawString(50, 700, f"Vendor: {vendor}")

    pdf.drawString(
        50, 670,
        f"Date: {invoice_date.strftime('%Y-%m-%d')}"
    )

    pdf.drawString(50, 640, f"Currency: {currency}")
    pdf.drawString(50, 610, f"Subtotal: Rs. {subtotal:.2f}")
    pdf.drawString(50, 580, f"Tax: Rs. {tax:.2f}")
    pdf.drawString(50, 550, f"Total: Rs. {total:.2f}")
    pdf.drawString(50, 520, f"Amount: Rs. {amount:.2f}")

    pdf.drawString(
        50, 470,
        "Thank you for your business!"
    )

    pdf.save()

# Save dataset
df = pd.DataFrame(data)

csv_path = os.path.join(
    BASE_DIR,
    "invoice_dataset.csv"
)

df.to_csv(csv_path, index=False)

print("20 invoices generated successfully!")
print("Invoice folder:", INVOICE_DIR)
print("Dataset saved:", csv_path)

print("\nDataset Preview:")
print(df.head(10).to_string(index=False))
