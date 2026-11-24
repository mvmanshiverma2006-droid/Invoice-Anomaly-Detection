import os
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE_DIR, "extracted_invoices.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "anomaly_results.csv")

# Load extracted invoice data
df = pd.read_csv(INPUT_FILE)

# Clean numeric columns
for col in ["Amount", "Subtotal", "Tax", "Total"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Amount"]).copy()

# Normalize invoice number and vendor
df["Invoice_No_Clean"] = (
    df["Invoice_No"].fillna("").astype(str).str.strip().str.upper()
)

df["Vendor_Clean"] = (
    df["Vendor"].fillna("").astype(str).str.strip().str.upper()
)

# ML anomaly detection
df["Amount_Log"] = np.log1p(df["Amount"])

model = IsolationForest(
    contamination=0.15,
    random_state=42
)

df["ML_Prediction"] = model.fit_predict(df[["Amount_Log"]])

df["ML_Anomaly"] = df["ML_Prediction"].map({
    1: "Normal",
    -1: "Suspicious"
})
# Vendor-wise Historical Amount Analysis
df["Vendor_High_Amount"] = False

for (vendor, currency), group in df.groupby(["Vendor", "Currency"]):
    if len(group) >= 3:
        median_amount = group["Amount"].median()

        threshold = median_amount * 2

        df.loc[group.index, "Vendor_High_Amount"] = (
            group["Amount"] > threshold
        )

# Duplicate detection
valid_invoice = (
    df["Invoice_No_Clean"].ne("")
    & df["Vendor_Clean"].ne("")
)

df["Duplicate_Invoice"] = False

df.loc[valid_invoice, "Duplicate_Invoice"] = (
    df.loc[valid_invoice]
    .duplicated(
        subset=["Vendor_Clean", "Invoice_No_Clean"],
        keep=False
    )
)

# Billing calculation validation
df["Billing_Mismatch"] = False

valid_billing = (
    df["Subtotal"].notna()
    & df["Tax"].notna()
    & df["Total"].notna()
)

calculated_total = df["Subtotal"] + df["Tax"]

df.loc[valid_billing, "Billing_Mismatch"] = (
    (calculated_total[valid_billing] - df.loc[valid_billing, "Total"]).abs() > 0.02
)

# Generate anomaly reasons
def get_anomaly_reason(row):

    reasons = []

    if row["Duplicate_Invoice"]:
        reasons.append("Duplicate invoice from same vendor")

    if row["ML_Anomaly"] == "Suspicious":
        reasons.append("Unusually high or abnormal invoice amount")
        
    if row["Vendor_High_Amount"]:
        reasons.append("Invoice amount is unusually high for this vendor")    

    if row["Billing_Mismatch"]:
        reasons.append("Subtotal and Tax do not match Total")

    if reasons:
        return "; ".join(reasons)

    return "No anomaly detected"

df["Anomaly_Reason"] = df.apply(get_anomaly_reason, axis=1)

# Final status
df["Final_Status"] = df.apply(
    lambda row: "Suspicious"
    if (
        row["Duplicate_Invoice"]
        or row["ML_Anomaly"] == "Suspicious"
        or row["Billing_Mismatch"]
        or row["Vendor_High_Amount"]
        
    )
    else "Normal",
    axis=1
)

# Remove temporary columns
df = df.drop(
    columns=["Invoice_No_Clean", "Vendor_Clean", "Amount_Log", "ML_Prediction"]
)

# Save results
df.to_csv(OUTPUT_FILE, index=False)

print("Anomaly Detection Completed Successfully!")

print("\nInvoice Analysis:")

print(df[[
    "Invoice_No",
    "Vendor",
    "Amount",
    "Duplicate_Invoice",
    "Billing_Mismatch",
    "ML_Anomaly",
    "Final_Status",
    "Anomaly_Reason"
]].to_string(index=False))

print("\nTotal Invoices:", len(df))
print("Suspicious Invoices:", (df["Final_Status"] == "Suspicious").sum())
print("Normal Invoices:", (df["Final_Status"] == "Normal").sum())
print("Duplicate Invoices:", df["Duplicate_Invoice"].sum())
print("Billing Mismatches:", df["Billing_Mismatch"].sum())

print("\nResults saved at:", OUTPUT_FILE)
print("\nResults saved at:", OUTPUT_FILE)
# Create Review Queue
REVIEW_FILE = os.path.join(BASE_DIR, "review_queue.csv")

review_columns = [
    "File_Name",
    "Invoice_No",
    "Vendor",
    "Amount",
    "Duplicate_Invoice",
    "ML_Anomaly",
    "Billing_Mismatch",
    "Vendor_High_Amount",
    "Anomaly_Reason",
    "Final_Status"
]

if "Missing_Fields" in df.columns:
    review_columns.insert(4, "Missing_Fields")

review_queue = df.loc[
    df["Final_Status"] == "Suspicious",
    review_columns
].copy()

review_queue.to_csv(REVIEW_FILE, index=False)

print("\nReview Queue created successfully!")
print("Invoices requiring manual review:", len(review_queue))
print("Review Queue saved at:", REVIEW_FILE)