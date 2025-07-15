# main.py
from services.billing import start_billing
from reports.sales_export import export_sales_csv

print("\n===== Customer Billing & Invoice Generator System =====")

def main_menu():
    while True:
        print("""
1. Generate New Invoice
2. Export Sales Report
3. Exit
        """)
        choice = input("Enter choice: ")

        if choice == '1':
            start_billing()
        elif choice == '2':
            export_sales_csv()
        elif choice == '3':
            print("Thank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
