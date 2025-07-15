from config.db_config import get_connection
from services.pdf_generator import generate_invoice_pdf

def start_billing():
    con = get_connection()
    cur = con.cursor()

    cust_id = int(input("Enter Customer ID: "))
    cur.execute("SELECT * FROM customers WHERE cust_id=%s", (cust_id,))
    cust = cur.fetchone()
    if not cust:
        print("Customer not found.")
        return

    invoice_items = []
    total = 0
    while True:
        prod_id = int(input("Enter Product ID (0 to finish): "))
        if prod_id == 0:
            break
        qty = int(input("Quantity: "))

        cur.execute("SELECT name, price, stock FROM products WHERE product_id=%s", (prod_id,))
        prod = cur.fetchone()
        if not prod or prod[2] < qty:
            print("Invalid product or insufficient stock.")
            continue

        subtotal = prod[1] * qty
        invoice_items.append((prod_id, qty, subtotal))
        total += subtotal

    cur.execute("INSERT INTO invoices (cust_id, total) VALUES (%s, %s)", (cust_id, total))
    invoice_id = cur.lastrowid

    for item in invoice_items:
        cur.execute("INSERT INTO invoice_items (invoice_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                    (invoice_id, item[0], item[1], item[2]))
        cur.execute("UPDATE products SET stock = stock - %s WHERE product_id=%s", (item[1], item[0]))

    con.commit()
    print(f"Invoice #{invoice_id} generated. Total: ₹{total:.2f}")
    generate_invoice_pdf(invoice_id)


