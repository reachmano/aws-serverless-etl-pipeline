
import csv
import logging
import os

# Create folders if they don't exist
os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logging.info("ETL pipeline started")

fieldnames = [
    "transaction_id",
    "customer_name",
    "amount",
    "status"
]

cleaned_data = []
rejected_data = []
seen_ids = set()

try:
    # STEP 1: EXTRACT
    with open(
        "data/transactions.csv",
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        lines = (line for line in file if line.strip())
        reader = csv.DictReader(lines)

        if not reader.fieldnames:
            raise ValueError("CSV header is missing")

        if not set(fieldnames).issubset(reader.fieldnames):
            raise ValueError("Required CSV columns are missing")

        transactions = list(reader)

    logging.info("Total records received: %s", len(transactions))

    # STEP 2: TRANSFORM
    for row_number, row in enumerate(transactions, start=2):

        try:
            transaction_id = (row["transaction_id"] or "").strip()
            customer_name = (row["customer_name"] or "").strip()
            raw_amount = (row["amount"] or "").strip()
            status = (row["status"] or "").strip().lower()

            if not transaction_id:
                raise ValueError("Missing transaction ID")

            if not customer_name:
                raise ValueError("Missing customer name")

            amount = float(raw_amount)

            if amount <= 0:
                raise ValueError("Amount must be greater than zero")

            if status != "success":
                raise ValueError("Transaction is not successful")

            if transaction_id in seen_ids:
                raise ValueError("Duplicate transaction ID")

            seen_ids.add(transaction_id)
            cleaned_data.append({
                "transaction_id": transaction_id,
                "customer_name": customer_name,
                "amount": amount,
                "status": status
            })

        except (ValueError, TypeError) as error:

            rejected_data.append({
                **{
                    key: row.get(key, "")
                    for key in fieldnames
                },
                "rejection_reason": str(error)
            })

            logging.warning(
                "Rejected row %s: %s",
                row_number,
                error
            )

    # STEP 3: LOAD CLEANED DATA
    with open(
        "output/cleaned_transactions.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

    # STEP 4: LOAD REJECTED DATA
    rejected_fields = fieldnames + ["rejection_reason"]

    with open(
        "output/rejected_transactions.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rejected_fields
        )
        writer.writeheader()
        writer.writerows(rejected_data)

    logging.info("Valid records: %s", len(cleaned_data))
    logging.info("Rejected records: %s", len(rejected_data))
    logging.info("ETL pipeline completed successfully")

    print("ETL Pipeline completed!")
    print("Total records:", len(transactions))
    print("Valid records:", len(cleaned_data))
    print("Rejected records:", len(rejected_data))

except FileNotFoundError:
    logging.exception("Input CSV file not found")
    print("ERROR: Input CSV file not found!")

except (ValueError, csv.Error):
    logging.exception("ETL input or CSV processing error")
    print("ERROR: Check the CSV file format and required columns.")

except OSError:
    logging.exception("File operation failed")
    print("ERROR: Unable to read or write a file.")
