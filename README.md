# Biometric Fraud Detection Project

This project analyzes biometric authentication data for fraud using Isolation Forest, DiD, and exports (CSV/ZIP/Base64).

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Add data to `/data/` or run `python examples/synthetic_generation.py`
3. Run: `python run_report.py`

## Structure
- `/data/`: Input/output files.
- `/modules/`: Core logic (loader, analysis, viz, exporter, report).
- `/examples/`: Synthetic data generation.
- `run_report.py`: End-to-end runner.

## Outputs
- `merged_income_auth_YYYY-MM-DD.csv`: Merged data with fraud predictions.
- `merged_income_auth_YYYY-MM-DD.zip`: Zipped version.
- `fraud_report.pdf`: Summary report with plots.

## License
MIT License with Ethical Use Notice (see headers). For research only; no real biometric data without consent.
pandas==2.2.2
numpy==1.26.4
scikit-learn==1.5.2
matplotlib==3.9.2
seaborn==0.13.2
reportlab==4.2.2
git add fraud_report.pdf  # Or merged_income_auth_2025-10-25.zip
git commit -m "Add fraud detection report (Oct 25, 2025)"
git push origin main
=== Starting Biometric Fraud Detection Pipeline ===
Loaded 1000 records
Fraud analysis complete
Results exported to output/merged_results_20251025_084500.csv
HTML/PDF report generated: output/report_20251025_084500.html
=== Pipeline completed successfully ===
<html>
<head><title>Biometric Fraud Report</title></head>
<body>
<h1>Biometric Fraud Detection Report</h1>
<p>Generated: 2025-10-25 08:45:00</p>
<p>Total records: 1000</p>
<p>Fraud cases: 100 (10.00%)</p>
<h2>Preview</h2>
<table class="table" border="0">
  <thead><tr><th>user_id</th><th>facial_score</th><th>...</th></tr></thead>
  <tbody><tr><td>0</td><td>57.91</td><td>...</td></tr></tbody>
</table>
<h2>Summary Observations</h2>
<pre>Total records analyzed: 1000
Detected fraud cases: 100 (10.00%)
Top suspects (user_id : anomaly_strength : facial_score : income):
 - 0 : 0.280 : 57.91 : 18234.12
 - 2 : 0.340 : 62.34 : 21456.78
 - 4 : 0.310 : 51.78 : 16789.01
 ...</pre>
</body>
</html>
0 8 * * * /absolute/path/to/virtualenv/bin/python /absolute/path/to/script/run_report.py
