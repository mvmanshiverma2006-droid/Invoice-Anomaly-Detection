import os
import fitz
import re
import pandas as pd
import pytesseract

from PIL import Image
from io import BytesIO

# Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Folder paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVOICE_DIR = os.path.join(BASE_DIR, "invoices")

extracted_data = []

# Function to extract amount
def extract_amount(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        return float(match.group(1).replace(",", ""))

    return None


# Read all PDF files
for file in os.listdir(INVOICE_DIR):

    if file.lower().endswith(".pdf"):

        pdf_path = os.path.join(INVOICE_DIR, file)
        doc = fitz.open(pdf_path)

        text = ""

        # Extract text from PDF or OCR
        for page in doc:

            page_text = page.get_text()

            if not page_text.strip():

                pix = page.get_pixmap(
                    matrix=fitz.Matrix(2, 2),
                    alpha=False
                )

                image = Image.open(
                    BytesIO(pix.tobytes("png"))
                )

                page_text = pytesseract.image_to_string(
                    image,
                    lang="eng"
                )

            text += page_text + "\n"

        doc.close()

        # Extract invoice number
        invoice_no = re.search(
            r"Invoice Number:\s*(\S+)",
            text,
            re.IGNORECASE
        )

        # Extract vendor
        vendor = re.search(
            r"Vendor:\s*(.+)",
            text,
            re.IGNORECASE
        )

        # Extract date
        date = re.search(
            r"Date:\s*(\d{4}-\d{2}-\d{2})",
            text,
            re.IGNORECASE
        )

        # Extract amounts
        subtotal = extract_amount(
            r"Subtotal:\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d{1,2})?)",
            text
        )

        tax = extract_amount(
            r"Tax:\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d{1,2})?)",
            text
        )

        total = extract_amount(
            r"(?<![A-Za-z])Total:\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d{1,2})?)",
            text
        )

        amount = extract_amount(
            r"Amount:\s*(?:Rs\.?|INR|₹)?\s*([\d,]+(?:\.\d{1,2})?)",
            text
        )

        # Use Amount as Total if Total is unavailable
        if total is None:
            total = amount

        # Keep Amount column for existing ML model
        if amount is None:
            amount = total

        # Detect currency
        if re.search(r"Rs\.?|INR|₹", text, re.IGNORECASE):
            currency = "INR"
        elif re.search(r"USD|\$", text, re.IGNORECASE):
            currency = "USD"
        elif re.search(r"EUR|€", text, re.IGNORECASE):
            currency = "EUR"
        else:
            currency = None

        # Identify missing fields
        missing_fields = []

        if not invoice_no:
            missing_fields.append("Invoice Number")

        if not vendor:
            missing_fields.append("Vendor")

        if not date:
            missing_fields.append("Date")

        if amount is None:
            missing_fields.append("Amount")

        if currency is None:
            missing_fields.append("Currency")

        extracted_data.append({

            "File_Name": file,

            "Invoice_No": invoice_no.group(1)
            if invoice_no else None,

            "Vendor": vendor.group(1).strip()
            if vendor else None,

            "Date": date.group(1)
            if date else None,

            "Currency": currency,

            "Subtotal": subtotal,

            "Tax": tax,

            "Total": total,

            "Amount": amount,

            "Missing_Fields": ", ".join(missing_fields),

            "Extraction_Status": "Complete"
            if not missing_fields else "Needs Review"

        })


# Save extracted data
df = pd.DataFrame(extracted_data)

output_path = os.path.join(
    BASE_DIR,
    "extracted_invoices.csv"
)

df.to_csv(output_path, index=False)

print("Invoice extraction completed successfully!")

print("Total invoices extracted:", len(df))

print("\nExtracted Data:")

print(df.head(10).to_string(index=False))

print("\nInvoices needing review:",
      (df["Extraction_Status"] == "Needs Review").sum())

print("\nResults saved at:", output_path)