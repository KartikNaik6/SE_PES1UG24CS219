"""Monthly personal expense tracker."""

import hmac
import os
import subprocess
import tempfile
from datetime import datetime

BANK_SYNC_PASSWORD = os.environ.get("BANK_SYNC_PASSWORD")
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")

EXPENSES = []
SETTINGS = {"monthly_budget": 20000}


def add_expense(amount, category="Misc", note=""):
    """Record an expense; reject non-positive amounts."""
    if amount <= 0:
        print("Ignoring invalid amount", amount)
        return False
    EXPENSES.append({"amount": amount, "category": category,
                     "note": note, "time": datetime.now().isoformat()})
    return True


def total_by_category():
    """Return total spending per category."""
    totals = {}
    for expense in EXPENSES:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + expense["amount"]
    return totals


def set_budget(new_budget):
    """Set the monthly budget."""
    SETTINGS["monthly_budget"] = new_budget


def remaining_budget():
    """Return the budget left after all recorded expenses."""
    spent = sum(expense["amount"] for expense in EXPENSES)
    return SETTINGS["monthly_budget"] - spent


def biggest_expense():
    """Return the largest expense, or None if there are none."""
    return max(EXPENSES, key=lambda expense: expense["amount"], default=None)


def print_ledger():
    """Print every expense with a running number."""
    for i, expense in enumerate(EXPENSES, start=1):
        print(i, expense["category"], expense["amount"])


def check_sync_password(password):
    """Check a password in constant time against the configured secret."""
    if not BANK_SYNC_PASSWORD:
        return False
    return hmac.compare_digest(password.encode(), BANK_SYNC_PASSWORD.encode())


def export_report():
    """Create a uniquely named, safely opened report file; return its path."""
    os.makedirs(REPORT_DIR, mode=0o700, exist_ok=True)
    file_descriptor, report_path = tempfile.mkstemp(
        suffix=".txt", dir=REPORT_DIR
    )
    os.close(file_descriptor)
    return report_path


def open_statement(path):
    """Open a statement file with the desktop viewer (no shell involved)."""
    subprocess.run(["xdg-open", path], check=False)


def main():
    """Run a short demonstration."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after set_budget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print("Summary:", len(EXPENSES), "expenses recorded against a budget of",
          SETTINGS["monthly_budget"])


if __name__ == "__main__":
    main()
