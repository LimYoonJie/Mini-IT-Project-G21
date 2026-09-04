from flask import Flask, render_template

app = Flask(__name__)


# Temporary product data
# This will eventually be replaced by the database.
products = [
    {
        "id": 1,
        "name": "Cat1",
        "category": "(category)",
        "price": 67.00,
        "stock": 32,
        "image": "https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif",
        "description": "temp desc."
    },
    {
        "id": 2,
        "name": "Cat2",
        "category": "(category)",
        "price": 67.00,
        "stock": 14,
        "image": "https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif",
        "description": "temp desc."
    },
    {
        "id": 3,
        "name": "Cat3",
        "category": "(category)",
        "price": 159.90,
        "stock": 0,
        "image": "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif",
        "description": "temp desc."
    },
    {
        "id": 4,
        "name": "Cat4",
        "category": "(category)",
        "price": 1299.90,
        "stock": 8,
        "image": "https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif",
        "description": "temp desc."
    }
]


# =========================
# CLIENT ROUTES
# =========================

@app.route("/")
def home():
    return render_template(
        "client/home.html",
        products=products
    )


@app.route("/products")
def product_list():
    return render_template(
        "client/products.html",
        products=products
    )


@app.route("/product/<int:product_id>")
def product_detail(product_id):

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        return "Product not found", 404

    return render_template(
        "client/product_detail.html",
        product=product
    )


@app.route("/cart")
def cart():
    return render_template("client/cart.html")


@app.route("/checkout")
def checkout():
    return render_template("client/checkout.html")


@app.route("/order-confirmation")
def order_confirmation():
    return render_template("client/order_confirmation.html")


@app.route("/login")
def login():
    return render_template("client/login.html")


@app.route("/register")
def register():
    return render_template("client/register.html")


@app.route("/profile")
def profile():
    return render_template("client/profile.html")


# =========================
# ADMIN ROUTES
# =========================

@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@app.route("/admin")
def admin_dashboard():
    return render_template(
        "admin/dashboard.html",
        products=products
    )


@app.route("/admin/products")
def admin_products():
    return render_template(
        "admin/products.html",
        products=products
    )


@app.route("/admin/products/add")
def add_product():
    return render_template("admin/add_product.html")


@app.route("/admin/products/edit/<int:product_id>")
def edit_product(product_id):

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product is None:
        return "Product not found", 404

    return render_template(
        "admin/edit_product.html",
        product=product
    )


@app.route("/admin/orders")
def admin_orders():
    return render_template("admin/orders.html")


@app.route("/admin/order/<int:order_id>")
def admin_order_detail(order_id):
    return render_template(
        "admin/order_detail.html",
        order_id=order_id
    )


@app.route("/admin/users")
def admin_users():
    return render_template("admin/users.html")


if __name__ == "__main__":
    app.run(debug=True)