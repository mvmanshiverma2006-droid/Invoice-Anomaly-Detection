from flask import Flask, render_template, send_file
import pandas as pd
import os
import shutil

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(
    BASE_DIR, "input_invoices", "anomaly_results.csv"
)
REVIEW_FILE = os.path.join(BASE_DIR, "input_invoices", "review_queue.csv")
EVALUATION_FILE = os.path.join(BASE_DIR, "input_invoices", "evaluation_report.txt")
@app.route("/")


def dashboard():
    df = pd.read_csv(DATA_FILE)

    total = len(df)
    normal = (df["Final_Status"] == "Normal").sum()
    suspicious = (df["Final_Status"] == "Suspicious").sum()
    high_amount = (df["Amount"] > 100000).sum()
    vendor_anomalies = (
    df["Anomaly_Reason"]
    .astype(str)
    .str.contains("unusually high for this vendor", case=False)
    .sum()
)

    duplicates = (
        df["Duplicate_Invoice"]
        .astype(str).str.lower().eq("true").sum()
    )

    source = os.path.join(
        BASE_DIR, "input_invoices", "visualizations"
    )
    destination = os.path.join(BASE_DIR, "static")

    graphs = [
        "invoice_status.png",
        "amount_distribution.png",
        "ml_anomaly_results.png",
        "duplicate_analysis.png"
    ]

    for graph in graphs:
        src = os.path.join(source, graph)
        dst = os.path.join(destination, graph)

        if os.path.exists(src):
            shutil.copy2(src, dst)

    invoices = df.fillna("").to_dict(orient="records")

    return render_template(
        "index.html",
        total=total,
        normal=normal,
        suspicious=suspicious,
        duplicates=duplicates,
        high_amount=high_amount,
vendor_anomalies=vendor_anomalies,
invoices=invoices
    )
    
    
    
    
@app.route("/download-report")
def download_report():
    return send_file(
        DATA_FILE,
        as_attachment=True,
        download_name="invoice_anomaly_report.csv",
        mimetype="text/csv"
    )
@app.route("/download-review")
def download_review():
    return send_file(
        REVIEW_FILE,
        as_attachment=True,
        download_name="review_queue.csv"
    )

@app.route("/download-evaluation")
def download_evaluation():
    return send_file(
        EVALUATION_FILE,
        as_attachment=True,
        download_name="evaluation_report.txt"
    )
    

if __name__ == "__main__":
    app.run(debug=True)