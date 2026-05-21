from flask import Flask, render_template, request, redirect, session
from db import init_db, get_conn
import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "volttrack_secret"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")

        return "Invalid username or password"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM equipment")
    total_equipment = cur.fetchone()[0]

    cur.execute("SELECT SUM(available) FROM equipment")
    available_equipment = cur.fetchone()[0] or 0

    cur.execute("SELECT COUNT(*) FROM borrow_records WHERE status='Borrowed'")
    borrowed_equipment = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM equipment WHERE LOWER(remarks) LIKE '%damaged%'")
    damaged_equipment = cur.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_equipment=total_equipment,
        available_equipment=available_equipment,
        borrowed_equipment=borrowed_equipment,
        damaged_equipment=damaged_equipment
    )


@app.route("/equipment")
def equipment():
    if "user_id" not in session:
        return redirect("/")

    search = request.args.get("search", "")

    conn = get_conn()
    cur = conn.cursor()

    if search:
        cur.execute("""
        SELECT * FROM equipment
        WHERE name LIKE ?
        OR category LIKE ?
        OR remarks LIKE ?
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))
    else:
        cur.execute("SELECT * FROM equipment")

    items = cur.fetchall()

    cur.execute("""
    SELECT borrow_records.id, users.username, equipment.name,
           borrow_records.quantity, borrow_records.date_borrowed,
           borrow_records.status
    FROM borrow_records
    JOIN users ON borrow_records.user_id = users.id
    JOIN equipment ON borrow_records.equipment_id = equipment.id
    WHERE borrow_records.status='Borrowed'
    """)
    records = cur.fetchall()

    conn.close()

    return render_template(
        "equipment.html",
        items=items,
        records=records,
        search=search
    )


@app.route("/add_equipment", methods=["POST"])
def add_equipment():
    if "user_id" not in session:
        return redirect("/")

    name = request.form["name"].strip()
    category = request.form["category"].strip()
    quantity = int(request.form["quantity"])
    remarks = request.form["remarks"].strip()

    image = request.files.get("image")
    image_filename = ""

    if image and image.filename != "":
        image_filename = secure_filename(image.filename)
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_filename))

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, quantity, available, image_filename
    FROM equipment
    WHERE LOWER(name) = LOWER(?)
    AND LOWER(category) = LOWER(?)
    """, (name, category))

    existing_item = cur.fetchone()

    if existing_item:
        equipment_id = existing_item[0]
        old_quantity = existing_item[1]
        old_available = existing_item[2]
        old_image = existing_item[3]

        new_quantity = old_quantity + quantity
        new_available = old_available + quantity
        final_image = image_filename if image_filename else old_image

        cur.execute("""
        UPDATE equipment
        SET quantity = ?, available = ?, remarks = ?, image_filename = ?
        WHERE id = ?
        """, (
            new_quantity,
            new_available,
            remarks,
            final_image,
            equipment_id
        ))

    else:
        cur.execute("""
        INSERT INTO equipment
        (name, category, quantity, available, remarks, image_filename)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            name,
            category,
            quantity,
            quantity,
            remarks,
            image_filename
        ))

    conn.commit()
    conn.close()

    return redirect("/equipment")


@app.route("/borrow/<int:equipment_id>", methods=["POST"])
def borrow(equipment_id):
    if "user_id" not in session:
        return redirect("/")

    borrow_quantity = int(request.form["borrow_quantity"])

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT available FROM equipment WHERE id=?", (equipment_id,))
    item = cur.fetchone()

    if item and borrow_quantity > 0 and item[0] >= borrow_quantity:
        cur.execute("""
        INSERT INTO borrow_records
        (user_id, equipment_id, quantity, date_borrowed, status)
        VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            equipment_id,
            borrow_quantity,
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Borrowed"
        ))

        cur.execute("""
        UPDATE equipment
        SET available = available - ?
        WHERE id = ?
        """, (borrow_quantity, equipment_id))

        conn.commit()

    conn.close()
    return redirect("/equipment")


@app.route("/return/<int:record_id>")
def return_item(record_id):
    if "user_id" not in session:
        return redirect("/")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT equipment_id, quantity
    FROM borrow_records
    WHERE id = ?
    """, (record_id,))

    record = cur.fetchone()

    if record:
        equipment_id = record[0]
        quantity = record[1]

        cur.execute("""
        UPDATE borrow_records
        SET date_returned = ?, status = 'Returned'
        WHERE id = ?
        """, (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            record_id
        ))

        cur.execute("""
        UPDATE equipment
        SET available = available + ?
        WHERE id = ?
        """, (quantity, equipment_id))

        conn.commit()

    conn.close()
    return redirect("/equipment")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)