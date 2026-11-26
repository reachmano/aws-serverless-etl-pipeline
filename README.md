<<<<<<< HEAD
Your local README content
=======
GitHub README content
>>>>>>> ...# AWS Serverless ETL Data Pipeline

## Project Overview

This project demonstrates a Python-based ETL pipeline designed to process synthetic banking transaction data.

The pipeline extracts transaction data from a CSV file, validates and transforms the records, and separates valid transactions from rejected records.

## Technologies Used

- Python
- CSV
- Git and GitHub
- AWS services (planned implementation)

## Project Structure

```text
aws-serverless-etl-pipeline/
├── data/
│   └── transactions.csv
├── src/
│   └── etl_pipeline.py
├── output/
├── logs/
├── requirements.txt
├── README.md
└── .gitignore
```

## ETL Process

### 1. Extract
- Read transaction records from a CSV file.
- Load records using Python's CSV module.

### 2. Transform
- Validate transaction IDs.
- Check customer names.
- Validate transaction amounts.
- Accept only successful transactions.
- Identify duplicate transaction IDs.
- Separate invalid records.

### 3. Load
- Save valid transactions to `output/cleaned_transactions.csv`.
- Save rejected transactions to `output/rejected_transactions.csv`.

## Error Handling and Logging

- Uses try-except blocks to handle errors.
- Logs pipeline execution details.
- Records rejected rows and their reasons.
- Handles missing input files and invalid CSV formats.

## How to Run the Project

1. Clone or download this repository.
2. Open the project folder in VS Code.
3. Activate your Python virtual environment.
4. Run:

```bash
python src/etl_pipeline.py
```

## Sample Input

The project uses synthetic banking transaction data. No real customer or banking information is used.

## Current Status

- [x] CSV extraction
- [x] Data validation
- [x] Duplicate removal
- [x] Error handling
- [x] Logging
- [ ] AWS S3 integration
- [ ] AWS Lambda integration
- [ ] AWS Glue Data Catalog
- [ ] Amazon Athena queries

## Future Enhancements

Integrate AWS services to build a fully serverless ETL pipeline using Amazon S3, AWS Lambda, AWS Glue, and Amazon Athena.