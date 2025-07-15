from fpdf import FPDF
from config.db_config import get_connection

def generate_invoice_pdf(invoice_id):
    con = get_connection()
    cur = con.cursor()

    cur.execute("SELECT i.invoice_id, c.name, c.phone, i.date, i.total FROM invoices i JOIN customers c ON i.cust_id = c.cust_id WHERE invoice_id=%s", (invoice_id,))
    inv = cur.fetchone()

    cur.execute("SELECT p.name, ii.quantity, ii.subtotal FROM invoice_items ii JOIN products p ON ii.product_id = p.product_id WHERE invoice_id=%s", (invoice_id,))
    items = cur.fetchall()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Invoice #{inv[0]}", ln=1)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Customer: {inv[1]} | Phone: {inv[2]}", ln=1)
    pdf.cell(200, 10, f"Date: {inv[3]}", ln=1)
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(80, 10, "Product", 1)
    pdf.cell(30, 10, "Quantity", 1)
    pdf.cell(40, 10, "Subtotal", 1)
    pdf.ln()

    pdf.set_font("Arial", size=12)
    for name, qty, sub in items:
        pdf.cell(80, 10, name, 1)
        pdf.cell(30, 10, str(qty), 1)
        pdf.cell(40, 10, f"Rs.{sub:.2f}", 1)
        pdf.ln()

    pdf.cell(110, 10, "Total", 1)
    pdf.cell(40, 10, f"Rs.{inv[4]:.2f}", 1)

    pdf.output(f"reports/invoices/invoice_{invoice_id}.pdf")
    print(f"PDF saved as invoice_{invoice_id}.pdf")


