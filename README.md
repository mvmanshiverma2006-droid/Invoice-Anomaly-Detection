# Automated Invoice Processing and Anomaly Detection

## Project Overview
This project is a Machine Learning-based application designed to automate invoice processing and identify suspicious invoices.

It extracts invoice information from PDF files, detects duplicate invoices, identifies unusual invoice amounts, and displays the results through an interactive Flask dashboard.

## Objectives
- Automate invoice data extraction from PDF files.
- Detect duplicate invoices.
- Identify suspicious invoices using Machine Learning.
- Visualize invoice analysis results.
- Generate downloadable anomaly reports.

## Technologies Used
- Python
- Machine Learning
- Pandas
- Scikit-learn
- Matplotlib
- Seaborn
- Flask
- PyMuPDF
- HTML
- CSS

## Key Features
1. PDF Invoice Data Extraction
2. Duplicate Invoice Detection
3. ML-Based Anomaly Detection using Isolation Forest
4. Invoice Analytics Dashboard
5. Invoice Search and Status Filter
6. Data Visualization
7. CSV Report Download

## Project Structure
```text
Invoice_Anomaly_Project/
|-- input_invoices/
|-- static/
|-- templates/
|-- app.py
|-- requirements.txt
|-- README.md
```

## How to Run the Project

1. Open the project folder in VS Code.

2. Activate the virtual environment:
   .\venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the Flask application:
   python app.py

5. Open the browser and visit:
   http://127.0.0.1:5000
## Output
The application displays invoice records, anomaly insights, duplicate invoice counts, and visualization graphs through a web dashboard.

## Evaluation Results
The project was evaluated using generated invoice datasets and a manually verified scanned invoice sample.

- Anomaly Detection Accuracy: 95%
- Precision: 83.33%
- Recall: 100%
- F1 Score: 90.91%
- Text PDF Extraction Accuracy: 100%
- Scanned PDF OCR Accuracy: 100%

The model successfully detected suspicious invoices with no false negatives in the evaluated dataset.

## Limitations
- The system is currently tested using a limited synthetic invoice dataset.
- Scanned invoice OCR accuracy is evaluated using only one manually verified sample.
- Machine Learning performance may vary with real-world invoice formats and data.
- A larger manually verified dataset is required for more reliable evaluation.
- OCR results may be affected by poor image quality or unclear text.

## Conclusion
This project demonstrates how Machine Learning can help automate invoice processing and identify potentially suspicious transactions, reducing manual effort and improving invoice analysis.

## Live Demo

Live Dashboard: https://invoice-anomaly-detection-p73l.onrender.com
