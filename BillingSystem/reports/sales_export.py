import csv
from config.db_config import get_connection



def export_sales_csv():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT invoice_id, cust_id, date, total FROM invoices")
    data = cur.fetchall()

    with open("reports/exports/sales_report.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Invoice ID", "Customer ID", "Date", "Total"])
        for row in data:
            writer.writerow(row)
    print("Sales report exported as sales_report.csv")

