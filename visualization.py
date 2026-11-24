
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "anomaly_results.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "visualizations")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv(FILE_PATH)

sns.set_theme(style="whitegrid")

# 1. Normal vs Suspicious Invoices
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="Final_Status")
plt.title("Normal vs Suspicious Invoices")
plt.xlabel("Invoice Status")
plt.ylabel("Number of Invoices")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "invoice_status.png"))
plt.show()
plt.close()

# 2. Invoice Amount Distribution
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x="Amount", bins=10, kde=True)
plt.title("Invoice Amount Distribution")
plt.xlabel("Invoice Amount")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "amount_distribution.png"))
plt.show()
plt.close()

# 3. Anomaly Detection Results
plt.figure(figsize=(7, 5))
sns.countplot(data=df, x="ML_Anomaly")
plt.title("ML Anomaly Detection Results")
plt.xlabel("ML Prediction")
plt.ylabel("Number of Invoices")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "ml_anomaly_results.png"))
plt.show()
plt.close()

# 4. Duplicate Invoice Analysis
plt.figure(figsize=(7, 5))
sns.countplot(
    data=df,
    x="Duplicate_Invoice",
    hue="Duplicate_Invoice",
    legend=False
)
plt.title("Duplicate Invoice Analysis")
plt.xlabel("Duplicate Invoice")
plt.ylabel("Number of Invoices")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "duplicate_analysis.png"))
plt.show()
plt.close()

print("All visualizations generated successfully!")
print("Graphs saved in:", OUTPUT_DIR)
