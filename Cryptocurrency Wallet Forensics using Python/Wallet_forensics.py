import json
import csv
import os
from decimal import Decimal, InvalidOperation
from collections import Counter
from datetime import datetime

def load_wallet_data(filename):
    """Load wallet data from a JSON file."""

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Wallet data must be a JSON object.")

        if not isinstance(data.get("transactions"), list):
            raise ValueError("Transactions must be a list.")

        if not isinstance(data.get("wallet_address"), str):
            raise ValueError("Wallet address is missing.")

        print("\nWallet data loaded successfully.")
        return data

    except FileNotFoundError:
        print("Error: Wallet data file not found.")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")

    except (OSError, ValueError) as error:
        print("Error:", error)

    return None

def classify_transaction(transaction, wallet_address):
    """Classify a transaction as incoming, outgoing or unrelated."""

    sender = transaction.get("from")
    receiver = transaction.get("to")

    if sender == wallet_address and receiver == wallet_address:
        return "Self-transfer"

    if receiver == wallet_address:
        return "Incoming"

    if sender == wallet_address:
        return "Outgoing"

    return "Unrelated"

def analyze_transactions(data):
    """Analyze transactions and calculate the net balance."""

    wallet_address = data["wallet_address"]
    transactions = data["transactions"]

    incoming_total = Decimal("0")
    outgoing_total = Decimal("0")
    fee_total = Decimal("0")

    records = []
    transaction_count = Counter()

    print("\n" + "=" * 65)
    print("            BITCOIN WALLET FORENSICS")
    print("=" * 65)

    print("Wallet identifier:", wallet_address)
    print("Total transaction records:", len(transactions))

    for number, transaction in enumerate(transactions, start=1):

        try:
            txid = str(transaction["txid"])
            sender = str(transaction["from"])
            receiver = str(transaction["to"])
            date = str(transaction["date"])

            amount = Decimal(str(transaction["amount_btc"]))
            fee = Decimal(str(transaction.get("fee_btc", 0)))

            if not amount.is_finite() or not fee.is_finite():
                raise ValueError("Amount and fee must be finite.")

            if amount < 0 or fee < 0:
                raise ValueError("Negative amounts or fees are invalid.")

            if not txid.strip():
                raise ValueError("Transaction ID is empty.")

            if not sender.strip() or not receiver.strip():
                raise ValueError("Sender or receiver is empty.")

        except (KeyError, ValueError, InvalidOperation,
                TypeError) as error:
            print("Skipping invalid transaction:", error)
            continue

        category = classify_transaction(
            transaction, wallet_address
        )

        # Calculate the wallet's net change
        if category == "Incoming":
            incoming_total += amount

        elif category == "Outgoing":
            outgoing_total += amount

        elif category == "Self-transfer":
            # The transfer itself does not change the balance.
            pass

        transaction_fee = Decimal("0")

        # Count fees only for outgoing or self-transfers
        # explicitly assumed to be paid by this wallet.
        if category in ("Outgoing", "Self-transfer"):
            transaction_fee = fee
            fee_total += fee

        transaction_count[category] += 1

        print("\nTransaction:", number)
        print("Transaction ID:", txid)
        print("Date:", date)
        print("From:", sender)
        print("To:", receiver)
        print("Type:", category)
        print("Amount:", amount, "BTC")
        print("Wallet fee:", transaction_fee, "BTC")

        records.append({
            "Transaction_ID": txid,
            "Date": date,
            "From": sender,
            "To": receiver,
            "Type": category,
            "Amount_BTC": str(amount),
            "Wallet_Fee_BTC": str(transaction_fee)
        })

    # Net change calculated from the supplied records.
    net_change = incoming_total - outgoing_total - fee_total

    return (
        records,
        incoming_total,
        outgoing_total,
        fee_total,
        net_change,
        transaction_count
    )

def generate_report(records, filename):
    """Export transaction details to a CSV file."""

    fields = [
        "Transaction_ID",
        "Date",
        "From",
        "To",
        "Type",
        "Amount_BTC",
        "Wallet_Fee_BTC"
    ]

    try:
        with open(filename, "w", newline="",
                  encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)

        print("\nTransaction report saved:", filename)

    except OSError as error:
        print("Could not save report:", error)

def display_summary(records, incoming, outgoing, fees,
                    net_change, transaction_count):
    """Display transaction statistics."""

    print("\n" + "=" * 65)
    print("                  FORENSIC SUMMARY")
    print("=" * 65)

    print("Valid records analyzed:", len(records))
    print("Incoming total:", incoming, "BTC")
    print("Outgoing total:", outgoing, "BTC")
    print("Wallet-paid fees:", fees, "BTC")
    print("Net balance change:", net_change, "BTC")

    print("\nTransaction classification:")

    for category, count in transaction_count.items():
        print(category, ":", count)

    print("\nAnalysis completed at:",
          datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    print("=" * 65)

def main():
    print("CRYPTOCURRENCY WALLET FORENSICS")
    print("--------------------------------")

    filename = input(
        "Enter wallet data filename (wallet_data.json): "
    ).strip()

    if not filename:
        filename = "wallet_data.json"

    if not os.path.isfile(filename):
        print("Error: File does not exist:", filename)
        return

    data = load_wallet_data(filename)

    if data is None:
        return

    results = analyze_transactions(data)

    records, incoming, outgoing, fees, net_change, counts = results

    generate_report(records, "transaction_report.csv")

    display_summary(
        records, incoming, outgoing, fees, net_change, counts
    )

if __name__ == "__main__":
    main()