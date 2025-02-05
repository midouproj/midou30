from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

app = Flask(__name__)

# بيانات وهمية للمشتري والبائع
buyers_data = {}
sellers_data = {}

# المشتري يدخل بياناته ويرسل المال
@app.route("/buyer", methods=["GET", "POST"])
def buyer():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        buyer_id = len(buyers_data) + 1
        buyers_data[buyer_id] = {"name": name, "email": email, "status": "Money Sent"}
        return redirect(url_for('seller', buyer_id=buyer_id))
    return render_template("buyer.html")

# البائع يدخل معرّف المشتري وبياناته الشخصية
@app.route("/seller/<int:buyer_id>", methods=["GET", "POST"])
def seller(buyer_id):
    if request.method == "POST":
        seller_name = request.form.get("seller_name")
        seller_lastname = request.form.get("seller_lastname")
        identity_file = request.files.get("identity_file")
        receipt_file = request.files.get("receipt_file")

        sellers_data[buyer_id] = {
            "seller_name": seller_name,
            "seller_lastname": seller_lastname,
            "identity_file": identity_file.filename,
            "receipt_file": receipt_file.filename,
            "status": "Processing"
        }

        # عملية رفع الوثائق
        identity_file.save(os.path.join("static", identity_file.filename))
        receipt_file.save(os.path.join("static", receipt_file.filename))

        # رسالة للمشتري
        buyers_data[buyer_id]["status"] = "Transaction Successful"
        return render_template("success_buyer.html", buyer_id=buyer_id)

    return render_template("seller.html", buyer_id=buyer_id)

# صفحة النجاح للبائع
@app.route("/success_buyer/<int:buyer_id>")
def success_buyer(buyer_id):
    return render_template("success_buyer.html", buyer_id=buyer_id)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))  # تأكد من استخدام المنفذ 3000
    app.run(host="0.0.0.0", port=port)
