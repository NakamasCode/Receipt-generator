from flask import render_template, request, session, redirect, url_for, flash, send_file, current_app as app
from .models import BusinessInfo, Transaction
from . import db
import cloudinary.uploader
from .utils import generate_receipt, generate_receipt_id

@app.route("/business", methods=["GET", "POST"])
def business():
    if session.get("business_set"):
        flash("Business details already set for this session!", "info")
        return redirect(url_for("index"))

    if request.method == "POST":
        name = request.form.get("name")
        contact = request.form.get("contact")
        email = request.form.get("email")
        logo_url = request.form.get("logo_url")  # fallback if no file

        # Handle file upload
        file = request.files.get('logo_file')
        if file and file.filename != '':
            result = cloudinary.uploader.upload(file, folder="johntimeless")
            logo_url = result['secure_url']

        # Store in session
        session["business_set"] = True
        session["business_name"] = name
        session["business_contact"] = contact
        session["business_email"] = email
        session["business_logo_url"] = logo_url

        flash("Business details saved for this session!", "success")
        return redirect(url_for("index"))

    return render_template("business.html")


@app.route("/", methods=["GET", "POST"])
def index():
    transactions = Transaction.query.order_by(Transaction.date_created.desc()).all()

    if request.method == "POST":
        txn_type = request.form.get("type")
        item_name = request.form.get("item_name")
        quantity = int(request.form.get("quantity") or 1)
        amount = float(request.form.get("amount"))
        description = request.form.get("description")
        customer_name = request.form.get("customer_name") if txn_type == "sales" else None
        phone_number = request.form.get("phone_number") if txn_type == "sales" else None

        txn = Transaction(
            receipt_id=generate_receipt_id(),  # ✅ generate receipt ID
            type=txn_type,
            item_name=item_name,
            quantity=quantity,
            amount=amount,
            description=description,
            customer_name=customer_name,
            phone_number=phone_number
        )
        db.session.add(txn)
        db.session.commit()
        flash("Transaction added!", "success")
        return redirect(url_for("index"))

    return render_template("index.html", transactions=transactions)


@app.route("/receipt/<int:txn_id>")
def receipt(txn_id):
    txn = Transaction.query.get_or_404(txn_id)
    pdf_buffer = generate_receipt(txn)
    return send_file(
        pdf_buffer,
        download_name=f"receipt_{txn.receipt_id}.pdf",
        mimetype="application/pdf"
    )


@app.route("/reset-demo")
def reset_demo():
    num_deleted = Transaction.query.delete()
    db.session.commit()
    session.clear()
    flash(f"Demo reset! {num_deleted} transactions deleted and session cleared.", "info")
    return redirect(url_for("index"))