# utils.py
import random
import string
from datetime import datetime
from io import BytesIO
from flask import session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import requests

def generate_receipt_id():
    """Generate a simple receipt ID with year prefix and 4 random alphanumeric chars."""
    year = datetime.now().year
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"{year}-{code}"

def generate_receipt(transaction):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    left = 50
    right = width - 50
    y = height - 60

    # -------------------------
    # BUSINESS INFO (session)
    # -------------------------
    business_name = session.get("business_name", "Your Business")
    business_contact = session.get("business_contact", "")
    business_email = session.get("business_email", "")
    business_logo_url = session.get("business_logo_url", None)

    # -------------------------
    # LOGO
    # -------------------------
    if business_logo_url:
        try:
            resp = requests.get(business_logo_url, stream=True, timeout=5)
            if resp.status_code == 200:
                logo = ImageReader(BytesIO(resp.content))
                c.drawImage(logo, left, y - 10, width=80, height=60, preserveAspectRatio=True, mask='auto')
        except Exception as e:
            print("Logo error:", e)

    # -------------------------
    # BUSINESS HEADER
    # -------------------------
    c.setFont("Helvetica-Bold", 18)
    c.drawRightString(right, y, business_name)
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawRightString(right, y, business_contact)
    y -= 15
    c.drawRightString(right, y, business_email)
    y -= 20
    c.line(left, y, right, y)

    # -------------------------
    # RECEIPT TITLE
    # -------------------------
    y -= 30
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left, y, "RECEIPT")
    c.setFont("Helvetica", 11)
    c.drawRightString(right, y, f"ID: {transaction.receipt_id}")  # ✅ show receipt_id

    # -------------------------
    # TRANSACTION INFO
    # -------------------------
    y -= 25
    c.setFont("Helvetica", 11)
    c.drawString(left, y, f"Date: {transaction.date_created.strftime('%Y-%m-%d %H:%M')}")
    y -= 18
    c.drawString(left, y, f"Type: {transaction.type.capitalize()}")
    if transaction.type == "sales":
        y -= 18
        c.drawString(left, y, f"Customer: {transaction.customer_name}")
        y -= 18
        c.drawString(left, y, f"Phone: {transaction.phone_number}")

    # Divider
    y -= 25
    c.line(left, y, right, y)

    # -------------------------
    # TABLE HEADER
    # -------------------------
    y -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left, y, "Item")
    c.drawString(left + 250, y, "Qty")
    c.drawRightString(right, y, "Amount (N)")
    y -= 10
    c.line(left, y, right, y)

    # Item row
    y -= 20
    c.setFont("Helvetica", 11)
    c.drawString(left, y, transaction.item_name)
    c.drawString(left + 250, y, str(transaction.quantity))
    c.drawRightString(right, y, f"N{transaction.amount:,.2f}")
    y -= 25
    c.line(left, y, right, y)

    # Total
    y -= 25
    c.setFont("Helvetica-Bold", 13)
    c.drawRightString(right, y, f"TOTAL: N{transaction.amount:,.2f}")

    if transaction.description:
        y -= 30
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(left, y, f"Note: {transaction.description}")

    # PAID STAMP
    c.saveState()
    c.setFont("Helvetica-Bold", 60)
    c.setFillGray(0.9)
    c.translate(width/2, height/2 + 50)
    c.rotate(30)
    c.drawCentredString(0, 0, "PAID")
    c.restoreState()

    # Footer
    y -= 50
    c.line(left, y, right, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width / 2, y, "Thank you for your business!")
    y -= 15
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, y, "Powered by JohnTimeless")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer