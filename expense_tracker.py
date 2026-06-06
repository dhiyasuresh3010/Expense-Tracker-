import json
import csv
import os

FILE_NAME = "expenses.json"


# ---------------- LOAD / SAVE ---------------- #

def load_expenses():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []
    return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as file:
        json.dump(expenses, file, indent=4)


# ---------------- ADD EXPENSE ---------------- #

def add_expense(expenses):
    print("\n--- ADD EXPENSE ---")

    date = input("Enter Date (DD-MM-YYYY): ").strip()
    category = input("Enter Category: ").strip().lower()

    try:
        amount = float(input("Enter Amount: ₹"))
    except ValueError:
        print("Invalid amount!")
        return

    description = input("Enter Description: ").strip()

    # Prevent duplicate entry
    for e in expenses:
        if (
            e["date"] == date and
            e["category"] == category and
            e["amount"] == amount and
            e["description"].lower() == description.lower()
        ):
            print("⚠ Duplicate expense not added!")
            return

    expenses.append({
        "date": date,
        "category": category,
        "amount": amount,
        "description": description
    })

    save_expenses(expenses)
    print("✔ Expense Added Successfully!")


# ---------------- VIEW ---------------- #

def view_expenses(expenses):
    print("\n===== EXPENSE LIST =====\n")

    if not expenses:
        print("No expenses found.")
        return

    for i, e in enumerate(expenses, start=1):
        print(f"{i}. {e['date']} | {e['category']} | ₹{e['amount']} | {e['description']}")


# ---------------- DELETE ---------------- #

def delete_expense(expenses):
    view_expenses(expenses)

    if not expenses:
        return

    try:
        index = int(input("\nEnter number to delete: ")) - 1

        if 0 <= index < len(expenses):
            removed = expenses.pop(index)
            save_expenses(expenses)
            print(f"✔ Deleted: {removed['description']}")
        else:
            print("Invalid number.")

    except ValueError:
        print("Invalid input.")


# ---------------- TOTAL ---------------- #

def show_total(expenses):
    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal Expenses: ₹{total:.2f}")


# ---------------- SEARCH ---------------- #

def search_by_category(expenses):
    category = input("Enter category: ").strip().lower()

    found = False
    print("\n===== RESULTS =====\n")

    for i, e in enumerate(expenses, start=1):
        if e["category"] == category:
            print(f"{i}. {e['date']} | {e['category']} | ₹{e['amount']} | {e['description']}")
            found = True

    if not found:
        print("No matching expenses found.")


# ---------------- CATEGORY SUMMARY ---------------- #

def category_summary(expenses):
    summary = {}

    for e in expenses:
        summary[e["category"]] = summary.get(e["category"], 0) + e["amount"]

    print("\n===== CATEGORY SUMMARY =====")

    for cat, total in summary.items():
        print(f"{cat}: ₹{total:.2f}")


# ---------------- HIGHEST ---------------- #

def highest_expense(expenses):
    if not expenses:
        print("No expenses found.")
        return

    highest = max(expenses, key=lambda x: x["amount"])

    print("\n===== HIGHEST EXPENSE =====")
    print(f"{highest['date']} | {highest['category']} | ₹{highest['amount']} | {highest['description']}")


# ---------------- EXPORT CSV ---------------- #

def export_csv(expenses):
    if not expenses:
        print("No data to export.")
        return

    with open("expenses.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])

        for e in expenses:
            writer.writerow([e["date"], e["category"], e["amount"], e["description"]])

    print("✔ Exported to expenses.csv")


# ---------------- MAIN MENU ---------------- #

def main():
    print("📊 Expense Tracker Started")

    expenses = load_expenses()

    while True:
        print("\n===== MENU =====")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Show Total")
        print("5. Search Category")
        print("6. Category Summary")
        print("7. Highest Expense")
        print("8. Export CSV")
        print("9. Exit")

        choice = input("Choose option: ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            delete_expense(expenses)
        elif choice == "4":
            show_total(expenses)
        elif choice == "5":
            search_by_category(expenses)
        elif choice == "6":
            category_summary(expenses)
        elif choice == "7":
            highest_expense(expenses)
        elif choice == "8":
            export_csv(expenses)
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    main()