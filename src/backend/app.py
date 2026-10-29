import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort, jsonify
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from db import get_connection, execute, is_sqlite, row_dict, rows_dict, init_preview_db

load_dotenv()
app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "local-demo-only-change-this-secret")
init_preview_db()

ROLE_LABELS = {
    "admin":"Administrator", "manager":"Manager", "kitchen":"Kitchen Staff",
    "cashier":"Cashier", "receptionist":"Receptionist", "customer":"Customer"
}

def query_all(sql, params=()):
    conn=get_connection()
    try:
        cur=execute(conn,sql,params); rows=cur.fetchall()
        result=rows_dict(rows)
        conn.commit()
        return result
    finally: conn.close()

def query_one(sql, params=()):
    rows=query_all(sql,params)
    return rows[0] if rows else None

def run_write(sql, params=()):
    conn=get_connection()
    try:
        cur=execute(conn,sql,params)
        last=getattr(cur,"lastrowid",None)
        conn.commit()
        return last
    except Exception:
        conn.rollback()
        raise
    finally: conn.close()

def current_user():
    return session.get("user")

def login_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        if not current_user():
            flash("Please sign in to continue.", "warning")
            return redirect(url_for("login", next=request.path))
        return fn(*args,**kwargs)
    return wrapper

def roles_required(*roles):
    def deco(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args,**kwargs):
            if current_user().get("role") not in roles:
                abort(403)
            return fn(*args,**kwargs)
        return wrapper
    return deco

def customer_id_for_user(user):
    if not user: return None
    row=query_one("SELECT id FROM customers WHERE user_id=%s" if os.getenv("DB_MODE","mysql")!="sqlite" else "SELECT id FROM customers WHERE user_id=?",(user["id"],))
    return row["id"] if row else None

def placeholder():
    return "?" if os.getenv("DB_MODE","mysql").lower()=="sqlite" else "%s"

@app.context_processor
def inject_globals():
    return {"logged_user":current_user(),"role_labels":ROLE_LABELS}

@app.route("/")
def index():
    categories=query_all("SELECT id,name FROM food_categories ORDER BY name")
    menu=query_all("SELECT m.id,m.name,m.description,m.price,m.is_vegetarian,c.name AS category FROM menu_items m LEFT JOIN food_categories c ON c.id=m.category_id WHERE m.is_available=1 ORDER BY m.id LIMIT 8")
    return render_template("index.html",categories=categories,menu=menu)

@app.route("/menu")
def menu():
    category=request.args.get("category","").strip()
    search=request.args.get("q","").strip()
    sql="SELECT m.id,m.name,m.description,m.price,m.is_vegetarian,c.name AS category,c.id AS category_id FROM menu_items m LEFT JOIN food_categories c ON c.id=m.category_id WHERE m.is_available=1"
    params=[]
    ph=placeholder()
    if category:
        sql += f" AND c.id={ph}"; params.append(category)
    if search:
        sql += f" AND (m.name LIKE {ph} OR m.description LIKE {ph})"; params += [f"%{search}%",f"%{search}%"]
    sql += " ORDER BY c.name,m.name"
    items=query_all(sql,tuple(params))
    categories=query_all("SELECT id,name FROM food_categories ORDER BY name")
    return render_template("menu.html",items=items,categories=categories,selected=category,q=search)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username","").strip()
        password=request.form.get("password","")
        user=query_one("SELECT id,username,password_hash,role,full_name,active FROM users WHERE username="+placeholder(),(username,))
        if user and user["active"] and check_password_hash(user["password_hash"],password):
            session.clear()
            session["user"]={k:user[k] for k in ("id","username","role","full_name")}
            flash(f"Welcome back, {user['full_name']}!", "success")
            role=user["role"]
            if role=="customer": return redirect(url_for("my_account"))
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been signed out.", "success")
    return redirect(url_for("index"))

@app.route("/dashboard")
@roles_required("admin","manager","kitchen","cashier","receptionist")
def dashboard():
    role=current_user()["role"]
    if role=="kitchen":
        orders=query_all("SELECT id,order_type,status,total_amount,created_at FROM food_orders WHERE status IN ('placed','confirmed','preparing','ready') ORDER BY created_at")
        return render_template("kitchen.html",orders=orders)
    if role=="receptionist":
        reservations=query_all("SELECT r.id,r.reservation_at,r.guests,r.status,c.full_name,c.phone,t.table_number FROM reservations r LEFT JOIN customers c ON c.id=r.customer_id LEFT JOIN dining_tables t ON t.id=r.table_id ORDER BY r.reservation_at DESC LIMIT 80")
        tables=query_all("SELECT * FROM dining_tables ORDER BY table_number")
        return render_template("reservations_admin.html",reservations=reservations,tables=tables)
    if role=="cashier":
        orders=query_all("SELECT o.id,o.status,o.total_amount,o.created_at,b.id AS bill_id,b.status AS bill_status,b.total_amount AS bill_total FROM food_orders o LEFT JOIN bills b ON b.order_id=o.id ORDER BY o.created_at DESC LIMIT 100")
        return render_template("cashier.html",orders=orders)
    stats={}
    if role in ("admin","manager"):
        stats["orders"]=query_one("SELECT COUNT(*) AS n FROM food_orders")["n"]
        stats["reservations"]=query_one("SELECT COUNT(*) AS n FROM reservations WHERE status IN ('pending','confirmed')")["n"]
        stats["menu_items"]=query_one("SELECT COUNT(*) AS n FROM menu_items WHERE is_available=1")["n"]
        stats["revenue"]=query_one("SELECT COALESCE(SUM(amount),0) AS n FROM payments WHERE status='completed'")["n"]
        recent=query_all("SELECT o.id,o.status,o.total_amount,o.created_at,c.full_name FROM food_orders o LEFT JOIN customers c ON c.id=o.customer_id ORDER BY o.created_at DESC LIMIT 8")
        popular=query_all("SELECT m.name,SUM(oi.quantity) AS quantity FROM order_items oi JOIN menu_items m ON m.id=oi.menu_item_id GROUP BY m.id,m.name ORDER BY quantity DESC LIMIT 5")
        return render_template("dashboard.html",stats=stats,recent=recent,popular=popular)
    abort(403)

@app.route("/reserve", methods=["GET","POST"])
def reserve():
    tables=query_all("SELECT id,table_number,capacity,area FROM dining_tables WHERE status='available' ORDER BY table_number")
    if request.method=="POST":
        name=request.form.get("name","").strip()
        phone=request.form.get("phone","").strip()
        email=request.form.get("email","").strip()
        guests=request.form.get("guests","2")
        at=request.form.get("reservation_at","")
        notes=request.form.get("notes","").strip()
        try:
            guests=int(guests)
            if not name or not phone or not at or guests<1 or guests>20: raise ValueError()
            if current_user() and current_user()["role"]=="customer":
                cid=customer_id_for_user(current_user())
            else:
                # For public reservations, create/reuse a customer by phone.
                existing=query_one("SELECT id FROM customers WHERE phone="+placeholder(),(phone,))
                if existing: cid=existing["id"]
                else:
                    uid=run_write("INSERT INTO users(username,password_hash,role,full_name,email,phone,active) VALUES("+",".join([placeholder()]*7)+")",
                        (f"guest_{phone}_{int(datetime.now().timestamp())}","!guest-account-no-login","customer",name,email,phone,1))
                    cid=run_write("INSERT INTO customers(user_id,full_name,phone,email) VALUES("+",".join([placeholder()]*4)+")",(uid,name,phone,email))
            # Let staff assign a table later; avoids false availability claims at booking time.
            run_write("INSERT INTO reservations(customer_id,table_id,reservation_at,guests,status,notes) VALUES("+",".join([placeholder()]*6)+")",(cid,None,at,guests,"pending",notes))
            flash("Reservation request received. Our team will confirm the table shortly.", "success")
            return redirect(url_for("index"))
        except (ValueError,TypeError):
            flash("Please provide a name, phone, valid date/time and party size.", "danger")
    return render_template("reserve.html",tables=tables)

@app.route("/order", methods=["GET","POST"])
def order():
    if not current_user() or current_user()["role"]!="customer":
        flash("Please sign in with a customer account to place an order.", "warning")
        return redirect(url_for("login"))
    items=query_all("SELECT id,name,price FROM menu_items WHERE is_available=1 ORDER BY name")
    if request.method=="POST":
        selected=[]
        for item in items:
            try: qty=int(request.form.get(f"qty_{item['id']}","0"))
            except ValueError: qty=0
            if qty>0:
                if qty>20:
                    flash("Maximum quantity per item is 20.", "danger"); return redirect(url_for("order"))
                selected.append((item,qty))
        if not selected:
            flash("Choose at least one menu item.", "warning"); return redirect(url_for("order"))
        cid=customer_id_for_user(current_user())
        subtotal=round(sum(float(i["price"])*q for i,q in selected),2)
        tax=round(subtotal*0.05,2)
        total=round(subtotal+tax,2)
        conn=get_connection()
        try:
            cur=execute(conn,"INSERT INTO food_orders(customer_id,order_type,status,total_amount,notes) VALUES("+",".join([placeholder()]*5)+")",(cid,"takeaway","placed",total,"Online demo order"))
            oid=cur.lastrowid
            for item,qty in selected:
                execute(conn,"INSERT INTO order_items(order_id,menu_item_id,quantity,unit_price) VALUES("+",".join([placeholder()]*4)+")",(oid,item["id"],qty,item["price"]))
            # MySQL trigger maintains the subtotal; the order header displays the billed total including tax.
            execute(conn,"UPDATE food_orders SET total_amount="+placeholder()+" WHERE id="+placeholder(),(total,oid))
            execute(conn,"INSERT INTO bills(order_id,subtotal,tax_amount,discount_amount,total_amount,status) VALUES("+",".join([placeholder()]*6)+")",(oid,subtotal,tax,0,total,"unpaid"))
            conn.commit()
            flash(f"Order #{oid} placed. Total including 5% demo tax: ₹{total:.2f}.", "success")
            return redirect(url_for("my_account"))
        except Exception:
            conn.rollback()
            flash("We couldn't place the order. Please try again.", "danger")
        finally: conn.close()
    return render_template("order.html",items=items)

@app.route("/my-account")
@roles_required("customer")
def my_account():
    cid=customer_id_for_user(current_user())
    orders=query_all("SELECT o.id,o.status,o.total_amount,o.created_at,b.status AS bill_status FROM food_orders o LEFT JOIN bills b ON b.order_id=o.id WHERE o.customer_id="+placeholder()+" ORDER BY o.created_at DESC",(cid,))
    reservations=query_all("SELECT id,reservation_at,guests,status,notes FROM reservations WHERE customer_id="+placeholder()+" ORDER BY reservation_at DESC",(cid,))
    return render_template("my_account.html",orders=orders,reservations=reservations)

@app.route("/admin/menu", methods=["GET","POST"])
@roles_required("admin","manager")
def manage_menu():
    if request.method=="POST":
        action=request.form.get("action")
        if action=="add":
            name=request.form.get("name","").strip()
            desc=request.form.get("description","").strip()
            price=request.form.get("price","0")
            cat=request.form.get("category_id")
            veg=1 if request.form.get("is_vegetarian") else 0
            try:
                price=float(price)
                if not name or price<=0: raise ValueError()
                run_write("INSERT INTO menu_items(category_id,name,description,price,is_vegetarian,is_available) VALUES("+",".join([placeholder()]*6)+")",(cat,name,desc,price,veg,1))
                flash("Menu item added.", "success")
            except Exception: flash("Unable to add item. Check the name, category and price.", "danger")
        elif action=="toggle":
            mid=request.form.get("id")
            item=query_one("SELECT is_available FROM menu_items WHERE id="+placeholder(),(mid,))
            if item:
                run_write("UPDATE menu_items SET is_available="+placeholder()+" WHERE id="+placeholder(),(0 if item["is_available"] else 1,mid))
                flash("Menu availability updated.", "success")
        return redirect(url_for("manage_menu"))
    items=query_all("SELECT m.*,c.name AS category FROM menu_items m LEFT JOIN food_categories c ON c.id=m.category_id ORDER BY m.id DESC")
    categories=query_all("SELECT id,name FROM food_categories ORDER BY name")
    return render_template("manage_menu.html",items=items,categories=categories)

@app.route("/admin/menu/<int:item_id>/edit", methods=["POST"])
@roles_required("admin","manager")
def edit_menu(item_id):
    name=request.form.get("name","").strip()
    try:
        price=float(request.form.get("price","0"))
        if not name or price<=0: raise ValueError()
        run_write("UPDATE menu_items SET name="+placeholder()+",price="+placeholder()+",description="+placeholder()+",category_id="+placeholder()+" WHERE id="+placeholder(),
                  (name,price,request.form.get("description",""),request.form.get("category_id"),item_id))
        flash("Menu item updated.", "success")
    except Exception: flash("Invalid menu item details.", "danger")
    return redirect(url_for("manage_menu"))

@app.route("/admin/reservations")
@roles_required("admin","manager","receptionist")
def manage_reservations():
    reservations=query_all("SELECT r.id,r.reservation_at,r.guests,r.status,r.notes,c.full_name,c.phone,t.table_number FROM reservations r LEFT JOIN customers c ON c.id=r.customer_id LEFT JOIN dining_tables t ON t.id=r.table_id ORDER BY r.reservation_at DESC")
    tables=query_all("SELECT id,table_number,capacity FROM dining_tables WHERE status='available' ORDER BY table_number")
    return render_template("reservations_admin.html",reservations=reservations,tables=tables)

@app.route("/admin/reservations/<int:rid>/status", methods=["POST"])
@roles_required("admin","manager","receptionist")
def reservation_status(rid):
    status=request.form.get("status")
    if status not in ("pending","confirmed","seated","completed","cancelled"):
        abort(400)
    table_id=request.form.get("table_id") or None
    run_write("UPDATE reservations SET status="+placeholder()+",table_id="+placeholder()+" WHERE id="+placeholder(),(status,table_id,rid))
    flash("Reservation updated.", "success")
    return redirect(request.referrer or url_for("manage_reservations"))

@app.route("/admin/orders")
@roles_required("admin","manager","kitchen","cashier")
def manage_orders():
    orders=query_all("SELECT o.id,o.status,o.order_type,o.total_amount,o.created_at,c.full_name FROM food_orders o LEFT JOIN customers c ON c.id=o.customer_id ORDER BY o.created_at DESC")
    return render_template("orders_admin.html",orders=orders)

@app.route("/admin/orders/<int:oid>/status", methods=["POST"])
@roles_required("admin","manager","kitchen")
def order_status(oid):
    status=request.form.get("status")
    allowed=("placed","confirmed","preparing","ready","served","cancelled")
    if status not in allowed: abort(400)
    run_write("UPDATE food_orders SET status="+placeholder()+" WHERE id="+placeholder(),(status,oid))
    flash("Order status updated.", "success")
    return redirect(request.referrer or url_for("manage_orders"))

@app.route("/admin/payments/<int:bill_id>", methods=["POST"])
@roles_required("admin","manager","cashier")
def record_payment(bill_id):
    method=request.form.get("method","cash")
    if method not in ("cash","upi","card","online"): abort(400)
    bill=query_one("SELECT id,total_amount,status FROM bills WHERE id="+placeholder(),(bill_id,))
    if not bill: abort(404)
    if bill["status"]=="paid":
        flash("This bill is already marked paid.", "warning")
        return redirect(request.referrer or url_for("dashboard"))
    conn=get_connection()
    try:
        execute(conn,"INSERT INTO payments(bill_id,amount,method,status,transaction_ref) VALUES("+",".join([placeholder()]*5)+")",(bill_id,bill["total_amount"],method,"completed",f"DEMO-{datetime.now().strftime('%Y%m%d%H%M%S')}"))
        execute(conn,"UPDATE bills SET status='paid' WHERE id="+placeholder(),(bill_id,))
        conn.commit()
        flash("Demo payment recorded. No real money was charged.", "success")
    except Exception:
        conn.rollback(); flash("Payment record could not be saved.", "danger")
    finally: conn.close()
    return redirect(request.referrer or url_for("dashboard"))

@app.route("/admin/employees")
@roles_required("admin","manager")
def employees():
    rows=query_all("SELECT e.id,e.full_name,e.role_title,e.phone,e.salary,e.hire_date,u.username,u.active FROM employees e LEFT JOIN users u ON u.id=e.user_id ORDER BY e.id")
    return render_template("employees.html",employees=rows)

@app.route("/admin/employees/<int:eid>/toggle", methods=["POST"])
@roles_required("admin")
def toggle_employee(eid):
    row=query_one("SELECT user_id FROM employees WHERE id="+placeholder(),(eid,))
    if row and row["user_id"]:
        run_write("UPDATE users SET active=CASE WHEN active=1 THEN 0 ELSE 1 END WHERE id="+placeholder(),(row["user_id"],))
        flash("Employee login access toggled.", "success")
    return redirect(url_for("employees"))

@app.route("/health")
def health():
    return jsonify({"status":"ok","app":"Bhoj Kolkata Restaurant Management System"})

@app.errorhandler(403)
def forbidden(e):
    return render_template("error.html",code=403,message="You do not have permission to access this page."),403

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html",code=404,message="The page you requested could not be found."),404

if __name__=="__main__":
    app.run(debug=os.getenv("FLASK_DEBUG","false").lower()=="true", host="127.0.0.1", port=int(os.getenv("PORT","5000")))
