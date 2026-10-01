import csv
import os
import sys
from datetime import datetime


def validate_row(row):
    if len(row) < 5:
        raise ValueError("missing field")

    transaction_id = row[0].strip()
    account_id = row[1].strip()
    transaction_type = row[2].strip().upper()
    amount_text = row[3].strip()
    timestamp = row[4].strip()

    if transaction_id == "" or account_id == "" or timestamp == "":
        raise ValueError("missing field")

    if transaction_type not in ("CREDIT", "DEBIT"):
        raise ValueError("invalid transaction type")

    amount = float(amount_text)
    if amount <= 0:
        raise ValueError("amount must be greater than 0")

    datetime.fromisoformat(timestamp)

    return account_id, transaction_type, amount


def main():
    try:
        if len(sys.argv) > 1:
            filename = sys.argv[1]
        else:
            filename = input().strip()

        if not os.path.isfile(filename):
            print("INPUT FILE NOT FOUND")
            return

        credit_rows = []
        debit_rows = []
        error_rows = []
        balances = {}

        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                try:
                    account, transaction_type, amount = validate_row(row)

                    if transaction_type == "CREDIT":
                        credit_rows.append(row)
                        balances[account] = balances.get(account, 0) + amount
                    else:
                        debit_rows.append(row)
                        balances[account] = balances.get(account, 0) - amount

                except (ValueError, IndexError) as error:
                    error_rows.append(row + [str(error)])

        with open("credit.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(credit_rows)

        with open("debit.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(debit_rows)

        with open("error.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(header + ["reason"])
            writer.writerows(error_rows)

        result = sorted(balances.items(), key=lambda x: (-abs(x[1]), x[0]))

        for account, balance in result:
            if balance.is_integer():
                balance = int(balance)
            print(account, balance)

        print("Files created: credit.csv, debit.csv, error.csv")

    except (OSError, StopIteration):
        print("INVALID INPUT")


if __name__ == "__main__":
    main()
